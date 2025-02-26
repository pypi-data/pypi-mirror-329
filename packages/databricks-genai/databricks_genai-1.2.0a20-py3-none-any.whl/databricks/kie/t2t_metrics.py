"""Implementation of task specific Text2Text metrics."""

from typing import Callable, List

import evaluate
from databricks.agents.evals import metric
from mlflow.evaluation import Assessment
from mlflow.metrics import MetricValue

from databricks.kie.eval_utils import PrimitiveTypes, fuzzy_match, normalized_match  # pylint: disable=ungrouped-imports
from databricks.kie.t2t_schema import InstructionType
from databricks.kie.text_utils import normalize_text

EXACT_MATCH_NAME = "classification_match"
FUZZY_MATCH_NAME = "fuzzy_match"
TOKENS_OVERLAP_FOR_SUBSPAN_EXTRACTION_NAME = "tokens_overlap_for_subspan_extraction"
ROUGE_L_SCORE_FOR_SUBSPAN_EXTRACTION_NAME = "rouge_L_score_for_subspan_extraction"
ROUGE_L_SCORE_FOR_SUMMARIZATION_NAME = "rouge_L_score_for_summarization"
BLEU_SCORE_FOR_SUMMARIZATION_NAME = "bleu_score_for_summarization"

# CLASSIFICATION METRICS


def exact_match(request: PrimitiveTypes, prediction: PrimitiveTypes, target: PrimitiveTypes, **kwargs) -> Assessment:
    """Normalized (+ exact) matching check between prediction and target."""
    if type(prediction) != type(target):  # pylint: disable=unidiomatic-typecheck
        return Assessment(name=kwargs.get("metric_name", EXACT_MATCH_NAME),
                          value=False,
                          rationale="Prediction and target are not the same type")

    # request is unused in this metric, but needs to be passed in
    match_assessment: Assessment = normalized_match(request, prediction, target)
    return Assessment(name=kwargs.get("metric_name", EXACT_MATCH_NAME),
                      value=match_assessment.value,
                      rationale=match_assessment.rationale)


# SUB-SPAN EXTRACTION METRICS


def fuzzy_match_score_with_target(request: PrimitiveTypes, prediction: PrimitiveTypes, target: PrimitiveTypes,
                                  **kwargs) -> Assessment:
    """Fuzzy string matching check between prediction and target."""
    if type(prediction) != type(target):  # pylint: disable=unidiomatic-typecheck
        return Assessment(name=kwargs.get("metric_name", FUZZY_MATCH_NAME),
                          value=False,
                          rationale="Prediction and target are not the same type")

    # request is unused in this metric, but needs to be passed in
    match_assessment: Assessment = fuzzy_match(request, prediction, target)
    return Assessment(name=kwargs.get("metric_name", FUZZY_MATCH_NAME),
                      value=match_assessment.value,
                      rationale=match_assessment.rationale)


def token_overlap_percentage_with_target(
        request: PrimitiveTypes,  # pylint: disable=unused-argument
        prediction: PrimitiveTypes,
        target: PrimitiveTypes,
        **kwargs) -> Assessment:
    """Token overlap check between prediction and target. Best for keyword extraction."""
    if not isinstance(prediction, str) or not isinstance(target, str):
        return Assessment(name=kwargs.get("metric_name", TOKENS_OVERLAP_FOR_SUBSPAN_EXTRACTION_NAME),
                          value=0.0,
                          rationale="Prediction and target are not strings")

    prediction_tokens = normalize_text(prediction).split()
    target_tokens = normalize_text(target).split()
    overlap = len(set(prediction_tokens) & set(target_tokens)) / len(set(prediction_tokens))
    return Assessment(name=kwargs.get("metric_name", TOKENS_OVERLAP_FOR_SUBSPAN_EXTRACTION_NAME),
                      value=int(overlap * 100),
                      rationale=f"{int(overlap * 100)}% of tokens in prediction overlap with the target")


def rouge_l_score_with_target(
        request: PrimitiveTypes,  # pylint: disable=unused-argument
        prediction: PrimitiveTypes,
        target: PrimitiveTypes,
        **kwargs) -> Assessment:
    """RougeL score check between prediction and target."""

    if not isinstance(prediction, str) or not isinstance(target, str):
        return Assessment(name=kwargs.get("metric_name", ROUGE_L_SCORE_FOR_SUBSPAN_EXTRACTION_NAME),
                          value=0.0,
                          rationale="Prediction and/or target are not strings")
    try:
        # TODO(Ricky): Try to find a more parallelizable way to calculate the Rouge L score
        rouge_calc: MetricValue = evaluate.load("rouge").compute(predictions=[prediction],
                                                                 references=[target])["rougeL"]
    except Exception as e:  # pylint: disable=broad-except
        return Assessment(name=kwargs.get("metric_name", ROUGE_L_SCORE_FOR_SUBSPAN_EXTRACTION_NAME),
                          value=None,
                          rationale=f'Error calculating Rouge L score with inputs "{prediction}" and "{target}": {e}')
    return Assessment(name=kwargs.get("metric_name", ROUGE_L_SCORE_FOR_SUBSPAN_EXTRACTION_NAME),
                      value=rouge_calc,
                      rationale=f"Rouge L score: {rouge_calc}")


# SUMMARIZATION METRICS


def bleu_score_with_target(
        request: PrimitiveTypes,  # pylint: disable=unused-argument
        prediction: PrimitiveTypes,
        target: PrimitiveTypes,
        **kwargs) -> Assessment:
    """We use BLEU to calculate the score for the prediction and target."""
    if not isinstance(prediction, str) or not isinstance(target, str):
        return Assessment(name=kwargs.get("metric_name", BLEU_SCORE_FOR_SUMMARIZATION_NAME),
                          value=0.0,
                          rationale="Prediction and/or target are not strings")
    if len(prediction.split()) < 4 or len(target.split()) < 4:
        return Assessment(
            name=kwargs.get("metric_name", BLEU_SCORE_FOR_SUMMARIZATION_NAME),
            value=0.0,
            rationale="Prediction and/or target have less than 4 tokens, which isn't enough to calculate a BLEU score")
    try:
        # TODO(Ricky): Try to find a more parallelizable way to calculate the BLEU score
        bleu_calc: MetricValue = evaluate.load("bleu").compute(predictions=[prediction], references=[target])["bleu"]
    except Exception as e:  # pylint: disable=broad-except
        return Assessment(name=kwargs.get("metric_name", BLEU_SCORE_FOR_SUMMARIZATION_NAME),
                          value=None,
                          rationale=f'Error calculating BLEU score with inputs "{prediction}" and "{target}": {e}')
    return Assessment(name=kwargs.get("metric_name", BLEU_SCORE_FOR_SUMMARIZATION_NAME),
                      value=bleu_calc,
                      rationale=f"Bleu score with prediction and target: {bleu_calc}")


# METRIC CREATION


def create_metric(fn: Callable[[PrimitiveTypes, PrimitiveTypes, PrimitiveTypes, str], float], metric_name: str):
    """Helper function to create an mlflow metric."""

    @metric(name=metric_name)
    def wrapper(request, response, expected_response):
        # Passing in the task specific metric name here since we could have the same metrics for different tasks
        return fn(request, response, expected_response, metric_name=metric_name)

    return wrapper


CLASSIC_METRICS = {
    InstructionType.subspan_extraction: [
        create_metric(token_overlap_percentage_with_target, TOKENS_OVERLAP_FOR_SUBSPAN_EXTRACTION_NAME),
        create_metric(rouge_l_score_with_target, ROUGE_L_SCORE_FOR_SUBSPAN_EXTRACTION_NAME),
    ],
    InstructionType.summarization: [
        create_metric(rouge_l_score_with_target, ROUGE_L_SCORE_FOR_SUMMARIZATION_NAME),
        create_metric(bleu_score_with_target, BLEU_SCORE_FOR_SUMMARIZATION_NAME),
    ],
}


def create_classic_metrics(task_type: InstructionType) -> List[metric]:
    """Create an mlflow metric given a task type."""
    return CLASSIC_METRICS.get(task_type, []) + [
        create_metric(exact_match, EXACT_MATCH_NAME),
        create_metric(fuzzy_match_score_with_target, FUZZY_MATCH_NAME),
    ]
