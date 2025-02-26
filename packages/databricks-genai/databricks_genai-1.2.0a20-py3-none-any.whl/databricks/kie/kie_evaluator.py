"""Evaluator class for Key Information Extraction (KIE) tasks."""

import json
import logging
import math
import re
import statistics
from typing import Any, Dict, Optional, Type, Union

import mlflow
import numpy as np
import pandas as pd
from databricks.agents.evals import metric  # pylint: disable=ungrouped-imports
from mlflow.evaluation import Assessment
from mlflow.models import EvaluationResult
from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo
from pyspark.sql.dataframe import DataFrame
from scipy.optimize import linear_sum_assignment

from databricks.kie.constants import MLFLOW_REGISTERED_MODEL_TAG
from databricks.kie.eval_utils import (PrimitiveTypes, correctness, exact_match, fuzzy_match, guideline_adherence,
                                       normalized_match)
from databricks.model_serving.utils import ModelSpecs
from databricks.model_training.api.utils import get_spark
from databricks.model_training.logging import temp_log_level

# Information on general metrics

OVERALL_SCORE = 'overall_score'
OVERALL_SCORE_RATIONALE = 'Overall score is the average of the individual field scores'
IS_SCHEMA_MATCH_RATIONALE = 'The schema of the response matches the expected schema.'
IS_JSON_PARSABLE_RATIONALE = 'The response is valid JSON.'
IS_NOT_SCHEMA_MATCH_RATIONALE = 'The schema of the response does not match the expected schema.'
IS_NOT_JSON_PARSABLE_RATIONALE = 'The response is not valid JSON.'

# Information on null metrics

TRUE_POSITIVE_NULL_RATE = 'true_positive_null_rate'
FALSE_POSITIVE_NULL_RATE = 'false_positive_null_rate'
FALSE_NEGATIVE_NULL_RATE = 'false_negative_null_rate'
NULL_FIELD_RATE_GT = "null_field_rate_gt"
NULL_FIELD_RATE_PRED = "null_field_rate_pred"

TRUE_POSITIVE_NULL_RATE_RATIONALE = ('The rate of correct null extractions is {rate} ({numerator}/{denominator}). ' +
                                     'Used to determine how much of nulls expected are correctly predicted. ' +
                                     'Calculated as (null-pred-null-gt / total null-gt)')
FALSE_POSITIVE_NULL_RATE_RATIONALE = (
    'The rate of false positive null extractions is {rate} ({numerator}/{denominator}). ' +
    'Used to determine if the model is predicting nulls that the ground truth claims to have valid extractions. ' +
    'Calculated as (null-pred-non-null-gt / total non-null-gt)')
FALSE_NEGATIVE_NULL_RATE_RATIONALE = (
    'The rate of false negative null extractions is {rate} ({numerator}/{denominator}). ' +
    'Used to determine if the model is predicting values that the ground truth claims to be null. ' +
    'Calculated as (non-null-pred-null-gt / total null-gt)')
NULL_FIELD_RATE_GT_RATIONALE = ('The rate of null fields in the ground truth is {rate} ({numerator}/{denominator}). ' +
                                'Used to determine what % of the extractions are null in the ground truth' +
                                'Calculated as (null-gt / null-gt + non-null-gt)')
NULL_FIELD_RATE_PRED_RATIONALE = ('The rate of null fields in the prediction is {rate} ({numerator}/{denominator}). ' +
                                  'Used to determine what % of the extractions are null in the prediction' +
                                  'Calculated as (null-pred / null-pred + non-null-pred)')

NULL_INFO_RESULTS_KEYS = [
    TRUE_POSITIVE_NULL_RATE, FALSE_POSITIVE_NULL_RATE, FALSE_NEGATIVE_NULL_RATE, NULL_FIELD_RATE_GT,
    NULL_FIELD_RATE_PRED
]

# Null metric helper keys

NULL_INFO_REQUIREMENTS_KEYS = [
    "total_nulls_gt", "total_non_nulls_gt", "null_pred_non_null_gt", "non_null_pred_null_gt", "null_pred_null_gt",
    "total_nulls_pred", "total_non_nulls_pred"
]

# TODO figure out how enums come in
AllowedInnerTypes = Union[PrimitiveTypes, BaseModel, list['AllowedInnerTypes']]
FieldTuple = tuple[AllowedInnerTypes, FieldInfo]

JUDGE_NAME_GUIDELINE = 'guideline_judge'
KIE_EVAL_METRIC_REGISTRY = {
    'exact_match': exact_match,
    'normalized_match': normalized_match,
    'fuzzy_match': fuzzy_match,
    'correctness': correctness,
    JUDGE_NAME_GUIDELINE: guideline_adherence,
}
DISALLOWED_NESTED_METRICS = {'correctness', JUDGE_NAME_GUIDELINE}


def get_default_metric_from_field(field_info: FieldInfo, gt_value: PrimitiveTypes, from_root: bool) -> str:
    """Select a default metric to use based on the field information

    Note: In the future, this routing could be done by an LLM, or other more sophisticated method.

    Args:
        field_info (FieldInfo): Pydantic field information.
        gt_value (PrimitiveTypes): Ground truth value.
        from_root (bool): Whether the field is a root field.

    Returns:
        str: Default metric to use.
    """

    del field_info  # Currently unused, but might be used for the description in the future

    if not isinstance(gt_value, str):
        return 'exact_match'

    gt_length = len(gt_value)

    # Completely arbitrary threshold
    if gt_length <= 10:
        return 'normalized_match'
    elif not from_root or gt_length <= 50:
        return 'fuzzy_match'
    else:
        return JUDGE_NAME_GUIDELINE


def parse_json_markdown(text: str) -> str:
    """Parse JSON from a markdown-formatted string.

    Allows text before or after the JSON block, and if no
    JSON block is found, returns the entire text.

    Args:
        text (str): Markdown-formatted string.

    Returns:
        str: JSON string.
    """
    pattern = r'^.*?```(?:json)?\s*(.*?)```\s*.*$'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def is_null_like(value: Any) -> bool:
    """Check if a value is null-like.

    Checks None, empty dict, empty list, and various string representations of null

    Args:
        value (any): Value to check.

    Returns:
        bool: True if value is null-like, False otherwise.
    """
    null_values = [None, '', 'null', 'none', 'nan', 'n/a', 'na', [], {}]
    is_none = value is None
    is_null_value = value in null_values
    lower_is_null_value = isinstance(value, str) and value.lower() in null_values
    is_nan = isinstance(value, float) and math.isnan(value)
    return is_none or is_null_value or lower_is_null_value or is_nan


class KIEEvaluator:
    """Evaluator for text to json output."""

    def __init__(self, schema: Type[BaseModel]):
        self.schema = schema

    def _create_null_information_assessments(self, null_info_requirements: dict[str, int]) -> dict[str, Assessment]:
        """Create null information assessments for a row."""

        # Helper function to format null metrics
        def _format_null_metrics(rate: float) -> float:
            return round(rate, 2)

        # Set the default of null metrics to None
        true_positive_null_assessment = Assessment(name=TRUE_POSITIVE_NULL_RATE,
                                                   value=None,
                                                   error_code="No nulls in ground truth")
        false_positive_null_assessment = Assessment(name=FALSE_POSITIVE_NULL_RATE,
                                                    value=None,
                                                    error_code="No nulls in ground truth")
        false_negative_null_assessment = Assessment(name=FALSE_NEGATIVE_NULL_RATE,
                                                    value=None,
                                                    error_code="No non-nulls in ground truth")
        null_field_rate_gt_assessment = Assessment(name=NULL_FIELD_RATE_GT,
                                                   value=None,
                                                   error_code="No nulls in ground truth")
        null_field_rate_pred_assessment = Assessment(name=NULL_FIELD_RATE_PRED,
                                                     value=None,
                                                     error_code="No nulls in prediction")
        # Calculate the necessary null metrics if there are any nulls in the ground truth
        if null_info_requirements["total_nulls_gt"] > 0:
            true_positive_null_rate = _format_null_metrics(null_info_requirements["null_pred_null_gt"] /
                                                           null_info_requirements["total_nulls_gt"])
            true_positive_null_assessment = Assessment(name=TRUE_POSITIVE_NULL_RATE,
                                                       value=true_positive_null_rate,
                                                       rationale=TRUE_POSITIVE_NULL_RATE_RATIONALE.format(
                                                           rate=true_positive_null_rate,
                                                           numerator=null_info_requirements["null_pred_null_gt"],
                                                           denominator=null_info_requirements["total_nulls_gt"]))
            false_negative_null_rate = _format_null_metrics(null_info_requirements["non_null_pred_null_gt"] /
                                                            null_info_requirements["total_nulls_gt"])
            false_negative_null_assessment = Assessment(name=FALSE_NEGATIVE_NULL_RATE,
                                                        value=false_negative_null_rate,
                                                        rationale=FALSE_NEGATIVE_NULL_RATE_RATIONALE.format(
                                                            rate=false_negative_null_rate,
                                                            numerator=null_info_requirements["non_null_pred_null_gt"],
                                                            denominator=null_info_requirements["total_nulls_gt"]))

        # Calculate the necessary null metrics if there are any non-nulls in the ground truth
        if null_info_requirements["total_non_nulls_gt"] > 0:
            false_positive_null_rate = _format_null_metrics(null_info_requirements["null_pred_non_null_gt"] /
                                                            null_info_requirements["total_non_nulls_gt"])
            false_positive_null_assessment = Assessment(name=FALSE_POSITIVE_NULL_RATE,
                                                        value=false_positive_null_rate,
                                                        rationale=FALSE_POSITIVE_NULL_RATE_RATIONALE.format(
                                                            rate=false_positive_null_rate,
                                                            numerator=null_info_requirements["null_pred_non_null_gt"],
                                                            denominator=null_info_requirements["total_non_nulls_gt"]))
        # Calculate the null field rate for the prediction
        total_pred_fields = null_info_requirements["total_nulls_pred"] + null_info_requirements["total_non_nulls_pred"]
        if total_pred_fields > 0:
            null_field_rate = _format_null_metrics(null_info_requirements["total_nulls_pred"] / total_pred_fields)
            null_field_rate_pred_assessment = Assessment(name=NULL_FIELD_RATE_PRED,
                                                         value=null_field_rate,
                                                         rationale=NULL_FIELD_RATE_PRED_RATIONALE.format(
                                                             rate=null_field_rate,
                                                             numerator=null_info_requirements["total_nulls_pred"],
                                                             denominator=total_pred_fields))
        # Calculate the null field rate for the ground truth
        total_gt_fields = null_info_requirements["total_nulls_gt"] + null_info_requirements["total_non_nulls_gt"]
        if total_gt_fields > 0:
            null_field_rate = _format_null_metrics(null_info_requirements["total_nulls_gt"] / total_gt_fields)
            null_field_rate_gt_assessment = Assessment(name=NULL_FIELD_RATE_GT,
                                                       value=null_field_rate,
                                                       rationale=NULL_FIELD_RATE_GT_RATIONALE.format(
                                                           rate=null_field_rate,
                                                           numerator=null_info_requirements["total_nulls_gt"],
                                                           denominator=total_gt_fields))
        return {
            TRUE_POSITIVE_NULL_RATE: true_positive_null_assessment,
            FALSE_POSITIVE_NULL_RATE: false_positive_null_assessment,
            FALSE_NEGATIVE_NULL_RATE: false_negative_null_assessment,
            NULL_FIELD_RATE_GT: null_field_rate_gt_assessment,
            NULL_FIELD_RATE_PRED: null_field_rate_pred_assessment
        }

    def evaluate_row(self, query: str, ground_truth_answer: str,
                     generated_answer: str) -> tuple[dict[str, Any], dict[str, Any]]:
        top_level_keys = self.schema.model_fields.keys()

        # Parse the provided strings into JSON strings
        gt_json_parsed = parse_json_markdown(ground_truth_answer)
        pred_json_parsed = parse_json_markdown(generated_answer)

        # Ground truth must be valid JSON
        try:
            gt_json_loaded = json.loads(gt_json_parsed)
        except json.JSONDecodeError as e:
            raise ValueError(f'Ground truth answer is not a valid JSON: {ground_truth_answer}') from e

        # Ground truth must match the provided schema
        try:
            gt_loaded = self.schema(**gt_json_loaded)
        except ValidationError as e:
            raise ValueError(f'Ground truth answer does not match the provided schema: {ground_truth_answer}') from e

        # Prediction may not have been valid JSON. Return early if it is not.
        try:
            pred_json_loaded = json.loads(pred_json_parsed)
        except json.JSONDecodeError as e:
            return {
                k: Assessment(name=k, value=0.0, rationale=IS_NOT_JSON_PARSABLE_RATIONALE) for k in top_level_keys
            }, {
                OVERALL_SCORE:
                    Assessment(name=OVERALL_SCORE, value=0.0, rationale=IS_NOT_JSON_PARSABLE_RATIONALE),
                'is_schema_match':
                    Assessment(name='is_schema_match', value=False, rationale=IS_NOT_JSON_PARSABLE_RATIONALE),
                'is_json_parsable':
                    Assessment(name='is_json_parsable', value=False, rationale=IS_NOT_JSON_PARSABLE_RATIONALE)
            }

        # Prediction may not match the provided schema. Return early if it is not.
        try:
            pred_loaded = self.schema(**pred_json_loaded)
        except ValidationError as e:
            return {
                k: Assessment(name=k, value=0.0, rationale=IS_NOT_SCHEMA_MATCH_RATIONALE) for k in top_level_keys
            }, {
                OVERALL_SCORE:
                    Assessment(name=OVERALL_SCORE, value=0.0, rationale=IS_NOT_SCHEMA_MATCH_RATIONALE),
                'is_schema_match':
                    Assessment(name='is_schema_match', value=False, rationale=IS_NOT_SCHEMA_MATCH_RATIONALE),
                'is_json_parsable':
                    Assessment(name='is_json_parsable', value=True, rationale=IS_NOT_SCHEMA_MATCH_RATIONALE)
            }

        # Both ground truth and prediction have been loaded into the provided schema and are pydantic objects.
        # TODO: Add an assert that the structures match at this point since all fields are required

        scored_output, null_info_requirements = self._scoring_helper_object(query, gt_loaded, pred_loaded, is_root=True)
        null_information = self._create_null_information_assessments(null_info_requirements)

        overall_score = statistics.mean([float(v.value) for v in scored_output.values()])
        overall_scoring = {
            OVERALL_SCORE: Assessment(name=OVERALL_SCORE, value=overall_score, rationale=OVERALL_SCORE),
            'is_schema_match': Assessment(name='is_schema_match', value=True, rationale=IS_SCHEMA_MATCH_RATIONALE),
            'is_json_parsable': Assessment(name='is_json_parsable', value=True, rationale=IS_JSON_PARSABLE_RATIONALE),
            **null_information
        }
        return scored_output, overall_scoring

    def _compute_pairwise_scores(
        self,
        query: str,
        gt_items: list[AllowedInnerTypes],
        pred_items: list[AllowedInnerTypes],
        gt_field_info: FieldInfo,
    ) -> np.ndarray:
        """Compute pairwise similarity scores between ground truth and predicted items."""
        scores = np.zeros((len(gt_items), len(pred_items)))
        null_info_matrix = [[None for _ in range(len(pred_items))] for _ in range(len(gt_items))]

        for i, gt_item in enumerate(gt_items):
            for j, pred_item in enumerate(pred_items):
                score_value, null_info_entry = self._scoring_helper_recurse(query, (gt_item, gt_field_info),
                                                                            (pred_item, gt_field_info))
                scores[i, j] = score_value.value
                null_info_matrix[i][j] = null_info_entry

        return scores, null_info_matrix

    def _compute_assignment(self, scores: np.ndarray) -> tuple[list[int], list[int]]:
        """Find optimal assignment using Hungarian algorithm."""
        row_ind, col_ind = linear_sum_assignment(scores, maximize=True)
        return row_ind.tolist(), col_ind.tolist()

    def _calculate_null_information_from_list(self, assignments,
                                              null_info_matrix: list[list[dict[str, int]]]) -> dict[str, int]:
        """Calculate null information from a list of items."""
        row_ind, col_ind = assignments
        matched_null_info = []
        for gt_idx, pred_idx in zip(row_ind, col_ind):
            matched_null_info.append(null_info_matrix[gt_idx][pred_idx])

        # Calculate each of the null information metrics for the entire list
        null_information = {k: sum(info[k] for info in matched_null_info) for k in NULL_INFO_REQUIREMENTS_KEYS}
        return null_information

    def _compute_precision_recall_f1(self, scores: np.ndarray,
                                     assignments: tuple[list[int], list[int]]) -> tuple[float, float, float]:
        """Compute precision and recall based on assignments."""
        row_ind, col_ind = assignments
        sum_scores = scores[row_ind, col_ind].sum()

        num_gt_items = scores.shape[0]
        num_pred_items = scores.shape[1]

        precision = sum_scores / num_pred_items
        recall = sum_scores / num_gt_items
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return precision, recall, f1

    def _scoring_helper_object(self,
                               query: str,
                               ground_truth_answer: BaseModel,
                               generated_answer: BaseModel,
                               is_root: bool = False) -> dict[str, Assessment]:
        results = {}
        null_information = {k: 0 for k in NULL_INFO_REQUIREMENTS_KEYS}
        for key_name in ground_truth_answer.model_dump():
            gt_value = getattr(ground_truth_answer, key_name)
            pred_value = getattr(generated_answer, key_name)

            gt_field_info = ground_truth_answer.model_fields[key_name]
            pred_field_info = generated_answer.model_fields[key_name]

            score, null_info_entry = self._scoring_helper_recurse(query, (gt_value, gt_field_info),
                                                                  (pred_value, pred_field_info),
                                                                  field_name=key_name,
                                                                  from_root=is_root)
            results[key_name] = Assessment(
                name=f'{key_name}',
                value=score.value,
                rationale=score.rationale,
            )
            for k in NULL_INFO_REQUIREMENTS_KEYS:
                null_information[k] += null_info_entry[k]

        return results, null_information

    def _score_null_presence(self, gt_value: PrimitiveTypes,
                             pred_value: PrimitiveTypes) -> tuple[Assessment, Dict[str, int]]:
        null_information = {k: 0 for k in NULL_INFO_REQUIREMENTS_KEYS}

        gt_is_null_like = is_null_like(gt_value)
        pred_is_null_like = is_null_like(pred_value)
        assert gt_is_null_like or pred_is_null_like, f'Unsupported null presence case: {gt_value} and {pred_value}'

        # Case 1: Both values are null-like
        if gt_is_null_like and pred_is_null_like:
            null_information["total_nulls_gt"] = 1
            null_information["total_nulls_pred"] = 1
            null_information["null_pred_null_gt"] = 1
            return Assessment(name='null_match', value=True, rationale='Both values are null-like'), null_information

        # Case 2: Ground truth is null-like but prediction is not
        if gt_is_null_like:
            null_information["total_nulls_gt"] = 1
            null_information["total_non_nulls_pred"] = 1
            null_information["non_null_pred_null_gt"] = 1
            return Assessment(name='null_match',
                              value=False,
                              rationale='expected_response is null-like but response is not'), null_information

        # Case 3: Prediction is null-like but ground truth is not
        if pred_is_null_like:
            null_information["total_non_nulls_gt"] = 1
            null_information["total_nulls_pred"] = 1
            null_information["null_pred_non_null_gt"] = 1
            return Assessment(name='null_match',
                              value=False,
                              rationale='response is null-like but expected_response is not'), null_information

        # Raise ValueError here because this should never happen
        raise ValueError(f'Unsupported null presence case: {gt_value} and {pred_value}')

    def _scoring_helper_recurse(self,
                                query: str,
                                ground_truth_answer: FieldTuple,
                                generated_answer: FieldTuple,
                                field_name: Optional[str] = None,
                                from_root: bool = False) -> tuple[Assessment, Dict[str, int]]:
        gt_value, gt_field_info = ground_truth_answer
        null_information = {k: 0 for k in NULL_INFO_REQUIREMENTS_KEYS}

        pred_value = generated_answer[0]

        # Early exit if either value is null-like
        gt_is_null_like = is_null_like(gt_value)
        pred_is_null_like = is_null_like(pred_value)
        if gt_is_null_like or pred_is_null_like:
            assessment, null_information = self._score_null_presence(gt_value, pred_value)
            return assessment, null_information

        if isinstance(gt_value, PrimitiveTypes):
            assert isinstance(pred_value, PrimitiveTypes)

            default_kie_eval_metric = get_default_metric_from_field(gt_field_info, gt_value, from_root)

            if gt_field_info.json_schema_extra is not None:
                eval_metric_string = str(
                    gt_field_info.json_schema_extra.get(  # type: ignore
                        'eval_metric', default_kie_eval_metric))
                eval_metric_kwargs: dict = gt_field_info.json_schema_extra.get('eval_metric_kwargs', {})  # type: ignore
            else:
                eval_metric_string = default_kie_eval_metric
                eval_metric_kwargs = {}

            if eval_metric_string == JUDGE_NAME_GUIDELINE:
                eval_metric_kwargs['field_name'] = field_name
                eval_metric_kwargs['field_definition'] = gt_field_info.description

            if eval_metric_string not in KIE_EVAL_METRIC_REGISTRY:
                raise ValueError(f'Unsupported evaluation metric: {eval_metric_string}')

            eval_metric_func = KIE_EVAL_METRIC_REGISTRY[eval_metric_string]

            assert isinstance(eval_metric_kwargs, dict)

            if eval_metric_string in DISALLOWED_NESTED_METRICS and not from_root:
                raise ValueError(f'Unsupported evaluation metric {eval_metric_string} for nested field')

            score = eval_metric_func(query, gt_value, pred_value, **eval_metric_kwargs)

            null_information["total_non_nulls_gt"] = 1
            null_information["total_non_nulls_pred"] = 1
            return score, null_information
        elif isinstance(gt_value, BaseModel):
            assert isinstance(pred_value, BaseModel)
            per_key_results, null_information = self._scoring_helper_object(query, gt_value, pred_value)
            result = statistics.mean([float(v.value) for v in per_key_results.values()])
            return Assessment(name='object_score', value=result,
                              rationale='Average of the individual field scores'), null_information
        elif isinstance(gt_value, list):
            assert isinstance(pred_value, list)
            pairwise_scores, null_info_matrix = self._compute_pairwise_scores(query, gt_value, pred_value,
                                                                              gt_field_info)
            assignments = self._compute_assignment(pairwise_scores)
            _, _, f1 = self._compute_precision_recall_f1(pairwise_scores, assignments)
            null_information = self._calculate_null_information_from_list(assignments, null_info_matrix)
            return Assessment(
                name='list_score',
                value=f1,
                rationale='Soft F1 score of the optimal pairwise assignment between list items'), null_information
        else:
            raise ValueError(f'Unsupported type: {type(gt_value)}')


def store_evaluation_metrics(df: pd.DataFrame, response_format: Type[BaseModel]) -> EvaluationResult:
    eval_class = KIEEvaluator(response_format)

    @metric
    def kie(request, response, expected_response):
        eval_output_per_key, eval_output_overall = eval_class.evaluate_row(request, expected_response, response)
        all_assessments = [eval_output_overall['is_schema_match']] + list(
            eval_output_per_key.values()) + [eval_output_overall[OVERALL_SCORE]]
        null_info_results_keys = [k for k in NULL_INFO_RESULTS_KEYS if k in eval_output_overall]
        all_assessments.extend(eval_output_overall[k] for k in null_info_results_keys)
        return all_assessments

    eval_result = mlflow.evaluate(
        model=None,
        data=df,
        model_type='databricks-agent',
        evaluator_config={'databricks-agent': {
            'metrics': [],
        }},
        extra_metrics=[kie],
    )

    return eval_result


def evaluate_model(df: DataFrame,
                   experiment_id: str,
                   model: ModelSpecs,
                   response_format: type[BaseModel],
                   run_name: Optional[str] = None,
                   run_id: Optional[str] = None) -> DataFrame:

    for required_column in ('request', 'response', 'expected_response'):
        if required_column not in df.columns:
            raise ValueError(f'`{required_column}` column is required for evaluation')

    model_df = df.toPandas()

    # Log each metric to mlflow
    start_kwargs = {}
    if run_id:
        start_kwargs['run_id'] = run_id
    elif run_name:
        start_kwargs['run_name'] = run_name
    with mlflow.start_run(experiment_id=experiment_id, **start_kwargs), temp_log_level('mlflow', logging.ERROR):
        mlflow.log_param(key='cost', value=model.cost_per_hour)
        mlflow.set_tag(MLFLOW_REGISTERED_MODEL_TAG, model.uc_schema)
        eval_result = store_evaluation_metrics(model_df, response_format)
        result_df = eval_result.tables['eval_results']

    spark = get_spark()
    return spark.createDataFrame(result_df)
