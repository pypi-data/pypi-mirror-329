"""Implements the optimization and data generation steps of the KIE pipeline"""
import json
import logging
import os
import time
from datetime import datetime
from functools import partial
from typing import Callable, ContextManager, Dict, List, Optional, Tuple, Type, cast

import mlflow
import pandas as pd
from mlflow.entities import Run as MlflowRun
from pydantic import BaseModel
from pyspark.sql.connect.dataframe import DataFrame

from databricks.kie.constants import MLFLOW_RESPONSE_FORMAT_FILE, MLFLOW_SYSTEM_PROMPT_FILE, MLFLOW_TRAILING_PROMPT_FILE
from databricks.kie.data_utils import (MIN_DOCS_TO_TRAIN, MIN_LABELED_TRAIN_SAMPLES, create_training_data,
                                       filter_valid_json, get_fewshot_examples, get_split_from_labeled,
                                       get_split_from_unlabeled, write_batch_to_cache)
from databricks.kie.inference_utils import format_ai_query
from databricks.kie.kie_evaluator import OVERALL_SCORE, evaluate_model
from databricks.kie.kie_schema import get_schema_hash
from databricks.kie.kie_state import KIEState
from databricks.kie.task_spec import KIETaskSpec
from databricks.model_serving.types.pt_endpoint import BaseEndpoint, PayGoEndpoint, ProvisionedThroughputEndpoint
from databricks.model_serving.utils import MODEL_CONTEXT_LENGTH, ModelSpecs, get_model_specs
from databricks.model_training.api import foundation_model as fm
from databricks.model_training.api.utils import get_schema_from_table, get_spark
from databricks.model_training.mlflow_utils import (DatasetSource, DatasetType, add_notebook_source, change_run_name,
                                                    get_mlflow_client, log_delta_table_source, log_uc_volume_source)
from databricks.model_training.types.run_status import RunStatus
from databricks.model_training.types.training_run import TrainingRun

logger = logging.getLogger(__name__)

DOLLAR_LIMIT_ENV_VAR = "DOLLAR_LIMIT_TESTING"


def get_run_name(alias: str, schema_hash: str, suffix: str) -> str:
    return f"kie-optimized-{alias}-{suffix}-{schema_hash}"


def get_eval_dataset_source(task_spec: KIETaskSpec) -> DatasetSource:
    if task_spec.labeled_dataset:
        return DatasetSource(DatasetType.DELTA_TABLE, task_spec.labeled_dataset)
    elif task_spec.unlabeled_delta_table:
        return DatasetSource(DatasetType.DELTA_TABLE, task_spec.unlabeled_delta_table)
    elif task_spec.unlabeled_dataset:
        return DatasetSource(DatasetType.UC_VOLUME, task_spec.unlabeled_dataset)
    else:
        # This should never happen
        raise ValueError("No dataset source provided")


class BaseDataGenerator:
    """Base class for generating data for training and validation"""

    def __init__(
        self,
        task_spec: KIETaskSpec,
        state: KIEState,
        model: ModelSpecs,
        use_provisioned_throughput: bool = True,
        use_ai_query: bool = False,
    ):
        self.task_spec = task_spec
        self.state = state
        self.model = model
        self.use_provisioned_throughput = use_provisioned_throughput
        self.use_ai_query = use_ai_query

    def _get_endpoint_context(self, teardown: bool = True) -> Callable[[], ContextManager[BaseEndpoint]]:
        """Get appropriate endpoint context based on configuration."""
        if self.use_provisioned_throughput:
            if not self.model.uc_schema:
                raise ValueError('UC schema required for provisioned throughput')
            return partial(ProvisionedThroughputEndpoint,
                           self.model.uc_schema,
                           model_version=self.model.version,
                           teardown_on_exit=teardown)

        if not self.model.endpoint:
            raise ValueError('Endpoint required for pay-as-you-go')
        return partial(PayGoEndpoint, self.model.endpoint)


class ValidationDataGenerator(BaseDataGenerator):
    """Generates validation data given the specified model, but only if there's no labeled data"""

    def __init__(
        self,
        task_spec: KIETaskSpec,
        state: KIEState,
        model: ModelSpecs,
        use_provisioned_throughput: bool = True,
        output_column: str = 'expected_response',
        use_ai_query: bool = False,
    ):
        super().__init__(task_spec,
                         state,
                         model,
                         use_provisioned_throughput=use_provisioned_throughput,
                         use_ai_query=use_ai_query)
        self.output_column = output_column

    def _get_labeled_validation_data(self) -> Optional[DataFrame]:
        """Get validation data from labeled dataset if available."""
        if not self.state.labeled_split_df:
            return None

        print("Using labeled data for validation set")
        return get_split_from_labeled(
            self.state.labeled_split_df,  # type: ignore
            'val',
            self.task_spec.labeled_dataset_text_column,
            self.task_spec.labeled_dataset_output_json_column)

    def get_validation_data(self) -> Tuple[DataFrame, bool]:
        """Get validation data from either labeled or unlabeled data.
        If the data is labeled, returns True as well, otherwise False"""
        # Try labeled data first
        val_df = self._get_labeled_validation_data()
        if val_df:
            return val_df, True
        return get_split_from_unlabeled(self.state.unlabeled_split_df, "val"), False

    def _generate_responses(self, requests: List[str], endpoint: BaseEndpoint) -> List[str]:
        """Generate responses using the endpoint."""
        responses = endpoint.generate_batch(requests,
                                            system_prompt=self.state.ground_truth_prompt,
                                            response_format=self.state.response_format,
                                            show_progress=False)
        total_tokens = sum(r.total_tokens for r in responses)
        logger.info(f'Total tokens used during generation: {total_tokens}')
        return [r.response for r in responses]

    def generate(self) -> None:
        """Generate validation data from either labeled or unlabeled data."""
        if not self.state.requires_val:
            return

        print('Getting validation data...')
        # Try labeled data first
        val_df, is_labeled = self.get_validation_data()
        if not is_labeled:
            print("Generating validation dataset...")
            print(f"Using {val_df.count()} documents from unlabeled dataset")

            # Generate responses
            endpoint_context = self._get_endpoint_context(teardown=False)
            if isinstance(endpoint_context, ProvisionedThroughputEndpoint):
                print("Creating an endpoint to hit. This may take a moment...")
            with endpoint_context() as endpoint:
                print("Extracting information from validation documents...")
                if self.use_ai_query:
                    print("Using ai_query to generate responses")

                    # Write the data to a table
                    val_df.createOrReplaceTempView("val_df")

                    # call ai_query to generate responses
                    # First, get or create UC table of validation data documents
                    # Now call ai_query to generate responses
                    val_df = endpoint.generate_ai_query(data_path="val_df",
                                                        system_prompt=self.state.ground_truth_prompt,
                                                        response_format=self.state.response_format,
                                                        output_column=self.output_column)
                    print(f"Finished generating {val_df.count()} responses from ai_query")
                else:
                    # Generate responses
                    as_pd = val_df.toPandas()
                    requests = as_pd["request"].tolist()
                    responses = self._generate_responses(requests, endpoint)

                    # Combine with original data
                    combined_df = pd.concat([as_pd, pd.DataFrame(responses, columns=[self.output_column])], axis=1)
                    spark = get_spark()
                    val_df = spark.createDataFrame(combined_df)

        # Cache result
        self.state.val_df = filter_valid_json(val_df, self.output_column, self.state.response_format)
        self.state.requires_val = False


def eval_single_model(df: DataFrame,
                      model: ModelSpecs,
                      prompt: str,
                      experiment_id: str,
                      response_format: Type[BaseModel],
                      run_id: str,
                      trailing_prompt: Optional[str] = None,
                      data_source: Optional[DatasetSource] = None) -> DataFrame:
    """
    Evaluate a single model using the provided validation data.

    Args:
        data_path: Path to validation data
        model: Model specifications
        prompt: Prompt to use for evaluation
        experiment_id: MLflow experiment ID
        response_format: Expected response format
        run_id: Optional MLflow run ID
        status: Optional status indicator for progress updates

    Returns:
        DataFrame containing evaluation results
    """

    if not model.uc_schema:
        raise ValueError('Model must have a UC schema defined')

    if trailing_prompt is None:
        trailing_prompt = prompt

    with ProvisionedThroughputEndpoint(model.uc_schema) as endpoint:
        df.createOrReplaceTempView("val_df")
        ai_query = format_ai_query("val_df", endpoint, prompt, trailing_prompt=trailing_prompt)
        spark = get_spark()

        model_df = spark.createDataFrame(spark.sql(ai_query).toPandas())
        # Log eval dataset to run
        if data_source and data_source.dataset_type == DatasetType.DELTA_TABLE:
            log_delta_table_source(run_id, data_source.dataset_path, name="Validation")
        elif data_source and data_source.dataset_type == DatasetType.UC_VOLUME:
            log_uc_volume_source(run_id, data_source.dataset_path, name="Validation")

        model_df = evaluate_model(model_df, experiment_id, model, response_format, run_id=run_id)
        return model_df  # type: ignore - DataFrame vs connect DataFrame T_T


def get_mlflow_run_by_name(run_name: str, experiment_id: str) -> Optional[MlflowRun]:
    """
    Find MLflow run by name in the given experiment.

    Args:
        run_name: Name of the run to find
        experiment_id: MLflow experiment ID

    Returns:
        MlflowRun if found, None otherwise
    """
    runs: List[MlflowRun] = mlflow.search_runs(experiment_ids=[experiment_id],
                                               filter_string=f"run_name='{run_name}'",
                                               output_format='list')  # type: ignore
    return runs[0] if runs else None


def get_fewshot_target_column(df: DataFrame) -> str:
    """ Get the response column from the grounding data.
    Prefers "expected_response" over "response" if both are present.
    """
    for col in ['expected_response', 'response']:
        if col in df.columns:
            return col
    raise ValueError('Response column not found in grounding data')


def update_run_with_required_data(run_id: str, system_prompt: str, trailing_prompt: str,
                                  response_format: Type[BaseModel]) -> None:
    """ Log the required data on a run that we will use for our state
    
    We log:
    1. The system prompt
    2. The trailing prompt
    3. The response format
    
    We also tag the run with:
    1. The endpoint uc_schema  TODO: This is currently in the eval code but should be here
    2. The datasets
    """

    # Log the prompts
    mlflow.log_text(system_prompt, MLFLOW_SYSTEM_PROMPT_FILE, run_id=run_id)
    mlflow.log_text(trailing_prompt, MLFLOW_TRAILING_PROMPT_FILE, run_id=run_id)

    # Log the response format
    mlflow.log_text(json.dumps(response_format.model_json_schema(), indent=2),
                    MLFLOW_RESPONSE_FORMAT_FILE,
                    run_id=run_id)


def evaluate_model_set(task_spec: KIETaskSpec, state: KIEState, models: List[ModelSpecs]) -> None:
    """
    Evaluate baseline models in both zero-shot and few-shot settings.

    Args:
        task_spec: Task specification (unused)
        state: Current task state
        models: List of models to evaluate
    """
    model_dfs = {}

    if not state.grounding_df:
        raise ValueError('Grounding data required for evaluation')

    response_column = get_fewshot_target_column(state.grounding_df)
    if state.num_fewshot_samples > 0:
        few_shot_examples = get_fewshot_examples(state.grounding_df,
                                                 state.num_fewshot_samples,
                                                 state.response_format,
                                                 response_column=response_column)
        fewshot_prompt = state.prompt_builder.build_prompt(few_shot_examples, include_markdown=True)
        run_fewshot = True
    else:
        fewshot_prompt = ""
        run_fewshot = False

    schema_hash = get_schema_hash(state.response_format)

    print("Evaluating a few initial models...")
    client = get_mlflow_client()
    for model in models:
        # Zero-shot evaluation
        run_name = get_run_name(model.alias, schema_hash, 'A')
        existing_run = get_mlflow_run_by_name(run_name, state.experiment.experiment_id)

        if not existing_run or not run_has_eval(existing_run.info.run_id):
            run_id = existing_run.info.run_id if existing_run else None
            if not run_id:
                run = client.create_run(experiment_id=state.experiment.experiment_id, run_name=run_name)
                run_id = run.info.run_id
                add_notebook_source(run_id)
            update_run_with_required_data(run_id, state.zeroshot_prompt, state.zeroshot_prompt, state.response_format)

            print(f"Evaluating {run_name}...")
            df = eval_single_model(state.val_df,
                                   model,
                                   state.zeroshot_prompt,
                                   state.experiment.experiment_id,
                                   state.response_format,
                                   run_id,
                                   data_source=get_eval_dataset_source(task_spec))

            model_dfs[run_name] = df
        else:
            print(f"Skipping eval for run {run_name} because it already exists")

        # Few-shot evaluation
        if not run_fewshot:
            continue

        # Few-shot evaluation
        run_name = get_run_name(model.alias, schema_hash, 'B')
        existing_run = get_mlflow_run_by_name(run_name, state.experiment.experiment_id)

        if not existing_run or not run_has_eval(existing_run.info.run_id):
            run_id = existing_run.info.run_id if existing_run else None
            if not run_id:
                run = client.create_run(experiment_id=state.experiment.experiment_id, run_name=run_name)
                run_id = run.info.run_id
                add_notebook_source(run_id)
            update_run_with_required_data(run_id, fewshot_prompt, state.zeroshot_prompt, state.response_format)

            print(f"Evaluating {run_name}...")
            df = eval_single_model(state.val_df,
                                   model,
                                   fewshot_prompt,
                                   state.experiment.experiment_id,
                                   state.response_format,
                                   run_id,
                                   trailing_prompt=state.zeroshot_prompt,
                                   data_source=get_eval_dataset_source(task_spec))

            model_dfs[run_name] = df
        else:
            print(f"Skipping eval for run {run_name} because it already exists")

    if not state.model_dfs:
        state.model_dfs = {}
    state.model_dfs.update(**model_dfs)


class TrainingDataGenerator(BaseDataGenerator):
    """Generates training data given the specified model, but only if there's not enough labeled data
    """

    def __init__(
        self,
        task_spec: KIETaskSpec,
        state: KIEState,
        model: ModelSpecs,
        optimized_models: List[ModelSpecs],
        use_provisioned_throughput: bool = True,
        min_labeled_samples: int = MIN_LABELED_TRAIN_SAMPLES,
        # TODO: If we have different sweeps per model, we should just add the information to the model spec instead
        num_learning_rates_per_model: int = 3,  # {5e-7, 1e-6, 1e-5} so 3 learning rates in total
        total_epochs_per_model: int = 6,  # {2, 4} are the epoch sweep so 6 epochs in total
        dollar_cost: int = 500,
        use_ai_query: bool = False,
    ):
        super().__init__(task_spec,
                         state,
                         model,
                         use_provisioned_throughput=use_provisioned_throughput,
                         use_ai_query=use_ai_query)
        self.min_labeled_samples = min_labeled_samples
        self.optimized_models = optimized_models
        self.num_learning_rates_per_model = num_learning_rates_per_model
        self.total_epochs_per_model = total_epochs_per_model
        if DOLLAR_LIMIT_ENV_VAR in os.environ:
            logger.info(f"Using environment variable {DOLLAR_LIMIT_ENV_VAR} to "
                        f"set dollar cost: ${os.environ[DOLLAR_LIMIT_ENV_VAR]}")
            self.dollar_cost = int(os.environ[DOLLAR_LIMIT_ENV_VAR])
        else:
            self.dollar_cost = dollar_cost

    def _get_labeled_training_data(self) -> Optional[Tuple[List[str], List[str]]]:
        """Extract training data from labeled dataset if available and sufficient."""
        if not self.state.labeled_split_df:
            return None

        train_df = get_split_from_labeled(self.state.labeled_split_df, 'train',
                                          self.task_spec.labeled_dataset_text_column,
                                          self.task_spec.labeled_dataset_output_json_column)

        if train_df.count() < self.min_labeled_samples:
            print(f"Only {train_df.count()} labeled documents found. "
                  "Using unlabeled dataset instead.")
            return None

        print(f"Using {train_df.count()} labeled documents for training")
        return tuple(
            zip(*train_df.select(
                self.task_spec.labeled_dataset_text_column,  # column for the request or data
                self.task_spec.labeled_dataset_output_json_column  # column for the expected response
            ).toPandas().values.tolist()))

    def _get_token_budget(self) -> int:
        """Get the token budget for the training data generation.

        We are currently training each model using the same number of tokens, but this could be better if
        we use an equivalent cost budget for each model instead of a token budget.

        If we have
        - N (token budget in millions of tokens),
        - C1 (cost of model 1 per million tokens), C2 (cost of model 2 per million tokens), etc.
        - E (total epochs across all trials of a model)
        - D (total dollar cost)

        Then we have the following equation:

        N*(C1 + C2 + ... + CN)*E = D

        This gives us N in millions of tokens. Theoretically, we could round down to the nearest million, but
        if we hit a case where we round down to 0 million, we will not be able to train the model.
        """
        total_cost_per_m_ft_tokens = sum(model.cost_per_m_ft_tokens for model in self.optimized_models)
        tokens_in_millions = self.dollar_cost / (self.num_learning_rates_per_model * self.total_epochs_per_model *
                                                 total_cost_per_m_ft_tokens)
        return int(tokens_in_millions * 1_000_000)

    def generate(self) -> None:
        """Generate training data from either labeled or unlabeled data."""
        if not self.state.requires_train_gen:
            return

        generated = True
        print("Getting training data...")

        # Try labeled data first
        labeled_data = self._get_labeled_training_data()
        # Temporarily disable using labeled training data until we test it more and implement cost bounding
        if False and labeled_data:  # pylint: disable=condition-evals-to-constant
            requests, responses = labeled_data
            print("Preparing labeled data for training...")
            write_batch_to_cache(self.state.ground_truth_prompt, requests, responses, self.state.response_format,
                                 self.state.train_jsonl_path)
        else:
            # Fall back to unlabeled data
            print("Generating training data from unlabeled data")
            endpoint_context = self._get_endpoint_context()
            if isinstance(endpoint_context, ProvisionedThroughputEndpoint):
                print("Creating an endpoint to hit. This may take a moment...")

            with endpoint_context() as endpoint:
                print("Extracting information from training documents...")
                output = create_training_data(unlabeled_split_df=self.state.unlabeled_split_df,
                                              prompt=self.state.ground_truth_prompt,
                                              response_format=self.state.response_format,
                                              train_jsonl_cache_path=self.state.train_jsonl_path,
                                              endpoint=endpoint,
                                              token_budget=self._get_token_budget(),
                                              use_ai_query=self.use_ai_query)
                if not output:
                    generated = False
                    # One of the two should be provided so this output should be valid
                    if self.task_spec.unlabeled_dataset:
                        unlabeled_dataset_str = f"Unlabeled dataset {self.task_spec.unlabeled_dataset}"
                    else:
                        unlabeled_dataset_str = f"Unlabeled delta table {self.task_spec.unlabeled_delta_table}"
                    print(f"{unlabeled_dataset_str} does not have enough " +
                          f"documents for training. We need at least {MIN_DOCS_TO_TRAIN + 25}")

        self.state.requires_train_gen = not generated


def launch_sweep(task_spec: KIETaskSpec, state: KIEState, models: List[ModelSpecs]) -> None:
    """Launch hyperparameter sweep.

    Launches training runs with different learning rates and epochs for each model.

    Args:
        task_spec: Task specification containing output location info
        state: Current task state with training data and experiment details
        models: List of models to sweep over

    Raises:
        ValueError: If models list is empty or no ft_model_name defined
        RuntimeError: If training data path or experiment name not set
    """

    if not state.train_jsonl_path:
        raise RuntimeError('Training data path not set')

    if not state.experiment.name:
        raise RuntimeError('Experiment name not set')

    register_to = '.'.join(task_spec.output_table.split('.')[:-1])
    suffixes = 'CDEFGHIJKLMNOPQRSTUVWXYZ'
    suffix_dict = dict(zip(range(1, len(suffixes) + 1), suffixes))
    schema_hash = get_schema_hash(state.response_format)
    for model in models:
        if not model.ft_model_name:
            raise ValueError(f'Model {model} has no ft_model_name defined')

        sweep_idx = 0

        # TODO:(DK) Update the sweep params when we turn PEFT on
        for lr in [5e-7, 1e-6, 1e-5]:
            for ep in [2, 4]:
                sweep_idx += 1
                run_name = get_run_name(model.alias, schema_hash, suffix_dict[sweep_idx])
                existing_run = get_mlflow_run_by_name(run_name, state.experiment.experiment_id)
                if existing_run:
                    print(f"Skipping launching run {run_name} because it already exists")
                    continue

                run = fm.create(
                    task_type="CHAT_COMPLETION",
                    model=model.ft_model_name,
                    train_data_path=state.train_jsonl_path,
                    experiment_path=state.experiment.name,
                    register_to=f"{register_to}.{run_name}-{state.experiment.experiment_id}",
                    learning_rate=lr,
                    training_duration=f"{ep}ep",
                    context_length=MODEL_CONTEXT_LENGTH,
                )
                assert run.run_id is not None
                update_run_with_required_data(run.run_id, state.ground_truth_prompt, state.ground_truth_prompt,
                                              state.response_format)

                # Update the run name to obscure it
                change_run_name(run.run_id, run_name)

                # Add notebook source since it's not passed through
                add_notebook_source(run.run_id)


def get_active_runs(experiment_id: str) -> List[TrainingRun]:
    return [run for run in fm.list(experiment_id=experiment_id) if run.status.before(RunStatus.COMPLETED)]


def run_has_eval(run_id: str, schema_hash: Optional[str] = None) -> bool:
    run = mlflow.get_run(run_id=run_id)
    run_name = cast(str, run.info.run_name)
    if schema_hash and not run_name.endswith(schema_hash):
        # If this is not from the same schema hash, we can skip it
        logger.info(f"Skipping eval for run {run_name} because it is not from the current schema")
        return True
    return run.data.metrics.get(OVERALL_SCORE) is not None


def get_runs_without_eval(experiment_id: str, schema_hash: Optional[str] = None) -> List[TrainingRun]:
    completed_runs = fm.list(experiment_id=experiment_id, statuses=[RunStatus.COMPLETED])
    return [run for run in completed_runs if run.run_id and not run_has_eval(run.run_id, schema_hash)]


class SweepEvaluator:
    """Follows runs in a sweep and evaluates them when they complete
    """

    def __init__(self, task_spec: KIETaskSpec, state: KIEState, timeout_minutes: int = 720):
        self.task_spec = task_spec
        self.state = state
        self.timeout_minutes = timeout_minutes
        self.start_time = datetime.now()

    def _get_model_mapping(self) -> Dict[str, ModelSpecs]:
        model_specs = get_model_specs()
        return {model.ft_model_name: model for model in model_specs.values() if model.ft_model_name is not None}

    def _create_model_details(self, run: MlflowRun, base_model: ModelSpecs) -> ModelSpecs:
        output_schema = get_schema_from_table(self.task_spec.output_table)
        run_name = cast(str, run.info.run_name)
        return ModelSpecs(
            name=run_name,
            endpoint='',
            cost_per_hour=base_model.cost_per_hour,
            ft_model_name=base_model.ft_model_name,
            is_hosted=False,
            uc_schema=f'{output_schema}.{run_name}-{self.state.experiment.experiment_id}',
        )

    def _eval_run(self, run: MlflowRun, model: ModelSpecs) -> DataFrame:
        model_details = self._create_model_details(run, model)

        return eval_single_model(self.state.val_df,
                                 model_details,
                                 self.state.ground_truth_prompt,
                                 self.state.experiment.experiment_id,
                                 self.state.response_format,
                                 run.info.run_id,
                                 data_source=get_eval_dataset_source(self.task_spec))

    def _is_timed_out(self) -> bool:
        elapsed = datetime.now() - self.start_time
        return elapsed.total_seconds() > (self.timeout_minutes * 60)

    def _check_run_deleted(self, run_id: str) -> bool:
        run = mlflow.get_run(run_id=run_id)
        if run.info.lifecycle_stage == "deleted":
            return True
        return False

    def evaluate_sweep(self) -> None:
        remaining = get_active_runs(self.state.experiment.experiment_id)
        schema_hash = get_schema_hash(self.state.response_format)
        run_eval = [
            r for r in get_runs_without_eval(self.state.experiment.experiment_id, schema_hash)
            if not self._check_run_deleted(r.run_id)
        ]  # type: ignore

        if not remaining and not run_eval:
            if not self.state.model_dfs:
                self.state.model_dfs = {}
            return

        model_map = self._get_model_mapping()
        run_to_model = {run.name: model_map.get(run.model or '') for run in remaining + run_eval}

        model_dfs = {}

        n_models = len(remaining)
        last_update = len(remaining)
        while not self._is_timed_out():
            logger.info(f"Checking runs: {remaining}")
            if len(remaining) < last_update:
                print(f"({n_models - len(remaining)}/{n_models}) Waiting for models to train...")
                last_update = len(remaining)
            # Process completed runs
            still_running = []
            for run in remaining:
                run = fm.get(run)
                if run.status is RunStatus.COMPLETED:
                    print(f"✓ Run {run.name} completed. Beginning evaluation")
                    run_eval.append(run)
                elif run.status is RunStatus.FAILED:
                    print(f"⨯ Run {run.name} failed")
                elif run.status is RunStatus.STOPPED:
                    print(f"⚠ Run {run.name} was canceled")
                else:
                    still_running.append(run)

            remaining = still_running

            # Evaluate completed runs
            if run_eval:
                print(f"Running evaluations for {len(run_eval)} models")
                if len(run_eval) > 1:
                    print("Evaluations are run in sequence, so this may take a moment")

            for run in run_eval:
                model = run_to_model[run.name]
                if model is None:
                    continue

                if not run.run_id:
                    raise RuntimeError(f"Run {run.name} has no run ID")

                if self._check_run_deleted(run.run_id):
                    # The run has been deleted
                    logger.info(f"Skipping eval for run {run.name} because it has been deleted")
                    continue

                mlflow_run = mlflow.get_run(run.run_id)
                print(f"Evaluating {mlflow_run.info.run_name}")
                model_dfs[mlflow_run.info.run_name] = self._eval_run(mlflow_run, model)
                print(f"Evaluations completed for {run.name}")  # TODO (TL): Add link to run evaluations page

            run_eval = []
            if not remaining:
                break

            time.sleep(60)

        self.state.model_dfs = model_dfs
