"""Module implementaion of entrypoint API for Text2Text."""

import functools
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import mlflow
import pandas as pd
import requests as request_lib
from databricks.agents.evals import judges, metric  # pylint: disable=ungrouped-imports
from mlflow import create_experiment, get_experiment_by_name, get_trace, start_run
from mlflow.evaluation import Assessment
from mlflow.models import infer_signature
from tqdm import tqdm

from databricks.kie.t2t_custom_model import CustomModel, ModelWrapper
from databricks.kie.t2t_evaluation_criteria_generator import (add_evaluation_criteria_from_preference_data,
                                                              generate_evaluation_criteria)
from databricks.kie.t2t_instruction_analyzer import populate_instruction_info
from databricks.kie.t2t_metrics import create_classic_metrics
from databricks.kie.t2t_models.t2t_model_registrations import create_t2t_model_list
from databricks.kie.t2t_models.t2t_model_registry import T2TModelConfig
from databricks.kie.t2t_schema import SideBySideResult, T2TSystemParams, T2TSystemResult, Text2TextTaskSpec
from databricks.kie.t2t_utils import (INSTRUCTION_AND_INPUT_PROMPT_TEMPLATE, generate_exp_name_from_instruction,
                                      get_registered_model_name, validate_secret_exists)
from databricks.kie.task_spec import get_default_experiment_name_with_suffix
from databricks.model_training.api.utils import get_host_and_token_from_env
from databricks.model_training.mlflow_utils import get_mlflow_client
from databricks.model_training.version import __version__

_MODEL_CONCURRENCY = 3


@dataclass
class PredictionResult:
    """Container for model prediction results."""
    prediction: str
    trace: Optional[str] = None


class Text2TextRunner:
    """
    A class to manage the Text2Text model lifecycle, including training, evaluation, and deployment.

    Main API:
    - compile(): Optimizes prompt / model given provided hyperparameters.
    - update_system_param(): Updates the state of the runner with new instruction, evaluation criteria, or example data.
    - evaluate_models(): Evaluates all models in the runner.
    - visualize_models(): Visualizes model predictions for a subset of test data.
    - deploy_model(): Deploys a model to a production endpoint.
    """
    MAX_EVAL_DATA = 100
    MAX_EXAMPLES_FOR_VISUALIZATION = 5

    def __init__(self, task_spec: Text2TextTaskSpec):
        """
        Initializes the Text2TextRunner with the provided parameters.

        Args:
            task_spec: Text2TextTaskSpec object containing the instruction, example data, and evaluation criteria
        """
        self.model_map: Dict[str, ModelWrapper] = {}
        self.default_model: Optional[ModelWrapper] = None
        self.prev_task_spec: Optional[Text2TextTaskSpec] = None
        self.prev_params: Optional[T2TSystemParams] = None
        self.custom_metrics = []

        self.current_task_spec = task_spec
        self.current_params = task_spec.to_system_param()

        experiment_name = task_spec.experiment_name
        if not experiment_name:
            experiment_suffix = generate_exp_name_from_instruction(self.current_params.instruction)
            experiment_name = get_default_experiment_name_with_suffix(f"t2t_{experiment_suffix}")
            print(f"Experiment name not provided. Creating new experiment: {experiment_name}")

        self.experiment_id = self._get_exp_id(experiment_name)
        self.mlflow_client = get_mlflow_client()

    def compile(self) -> T2TSystemResult:
        # get common data shared between previous state and new state.
        common_data = []
        prev_res = []
        if self.prev_params:
            print("Generating response for previous state for side by side comparison...")
            # generate req/response for previous state. This will be used to compare with current state.
            common_data = self.prev_params.get_sxs_data(self.current_params)[0:self.MAX_EXAMPLES_FOR_VISUALIZATION]
            assert self.default_model is not None
            prev_res = self._visualize_model(self.default_model, data=common_data)

        print("Compiling new system...")
        # Construct evaluation criteria. Infer from examples if not provided.
        if not self.current_params.evaluation_criteria:
            print("Inferring evaluation criteria automatically...")
            inferred_eval_criteria = generate_evaluation_criteria(self.current_params.instruction,
                                                                  self.current_params.labelled_test_examples)
            self.current_params.evaluation_criteria = inferred_eval_criteria
            self.current_task_spec.evaluation_criteria = inferred_eval_criteria

        # If user provided labels or corrections, then add them to the evaluation criteria.
        if self.current_params.preference_data:
            new_eval_criteria = add_evaluation_criteria_from_preference_data(
                self.current_params.instruction,
                self.current_params.evaluation_criteria,
                self.current_params.preference_data,
            )
            self.current_params.evaluation_criteria = new_eval_criteria
            self.current_task_spec.evaluation_criteria = new_eval_criteria

        self._create_custom_metrics()
        populate_instruction_info(self.current_params)

        self._create_classic_metrics()
        self.create_models()

        # generate response for common data for current state -- to be used for SxS comparison.
        current_res = []
        if prev_res:
            assert common_data and self.default_model is not None
            print("Getting new system response for side by side comparison..")
            current_res = self._visualize_model(self.default_model, data=common_data)
        return self._get_model_result(prev_res, current_res)

    def _get_model_result(self, prev_result, current_result) -> T2TSystemResult:
        sxs_results = None
        if self.prev_params:
            sxs_results = []
            assert prev_result and current_result
            for prev, current in zip(prev_result, current_result):
                sxs_results.append(
                    SideBySideResult(request=prev['input'],
                                     previous_response=prev['model_output'],
                                     current_response=current['model_output']))

        assert self.default_model is not None

        print("Visualizing model results..")
        data = [{
            'request': datum[0],
            'response': datum[1]
        } for datum in self.current_params.labelled_test_examples[0:self.MAX_EXAMPLES_FOR_VISUALIZATION]]

        examples = self._visualize_model(self.default_model, data=data)

        print("Evaluating default model...")
        eval_result = self._evaluate_model(self.default_model, data=data)
        models = [model.run_name for model in self.model_map.values()]
        return T2TSystemResult(
            eval_result=eval_result,
            examples=examples,
            sxs_result=sxs_results,
            current_task_spec=self.current_task_spec,
            experiment_id=self.experiment_id,
            model_candidates=models,
            default_model=self.default_model.run_name,
            instruction_info=self.current_params.instruction_info,
        )

    def get_system_param(self) -> Dict[str, Any]:
        models = list(self.model_map.keys())

        return {
            "instruction": self.current_params.instruction,
            "eval_criteria": self.current_task_spec.evaluation_criteria,
            "example_data": self.current_params.labelled_test_examples[:self.MAX_EXAMPLES_FOR_VISUALIZATION],
            "experiment_id": self.experiment_id,
            "model_candidates": models,
            "instruction_info": self.current_params.instruction_info,
        }

    def update_system_param(self, new_spec: Text2TextTaskSpec):
        """Updates the state of the runner with new Text2Text spec."""
        if new_spec.experiment_name is not self.current_task_spec.experiment_name:
            raise ValueError("Experiment name cannot be updated.")
        new_system_param = new_spec.to_system_param()
        self.prev_params = self.current_params
        self.prev_task_spec = self.current_task_spec
        self.current_task_spec = new_spec
        self.current_params = new_system_param
        return self.compile()

    def evaluate_models(self):
        """Evaluates all models in the runner using the provided evaluation criteria."""
        result = {}
        if not self.current_task_spec.evaluation_criteria:
            raise ValueError("Evaluation criteria is not provided. Make sure to call `compile()` API.")

        for model_wrapper in self.model_map.values():
            model_eval = self._evaluate_model(model_wrapper)
            result[model_wrapper.run_name] = model_eval
        return result

    def visualize_models(self):
        """Runs a subset of test data through each model and returns the results."""
        result = {}
        for model_wrapper in self.model_map.values():
            result[model_wrapper.run_name] = self._visualize_model(model_wrapper)
        return pd.DataFrame.from_dict(result)

    def deploy_model(self, run_name: str, endpoint_name: str, secret_scope: str, secret_key: str):
        """Deploys a model to a production endpoint using the provided secret.

        Args:
            run_name: The run name of the model to deploy.
            endpoint_name: The name of the endpoint to deploy.
            secret_scope: The secret scope containing the secret.
            secret_key: The secret key to use for the deployment.
        """
        if not validate_secret_exists(secret_scope, secret_key):
            raise ValueError(f"Secret {secret_key} in scope {secret_scope} does not exist.")

        model_wrapper = None
        model_wrapper = self.model_map.get(run_name, None)
        if not model_wrapper:
            raise ValueError(
                f"invalid model descriptor.. input: `{run_name}` candidates: {list(self.model_map.keys())}")

        model_url = model_wrapper.get_model_path()
        production_model = mlflow.pyfunc.load_model(model_url)
        api_url, api_token = get_host_and_token_from_env()
        data = {
            "name": endpoint_name,
            "config": {
                "served_entities": [{
                    "entity_name": model_wrapper.registered_model_name,
                    "entity_version": '1',
                    "workload_size": "Small",
                    "scale_to_zero_enabled": False,
                    "environment_vars": {
                        "DATABRICKS_HOST": api_url,
                        "DATABRICKS_TOKEN": "{{" + f"secrets/{secret_scope}/{secret_key}" + "}}",
                    }
                }]
            }
        }

        headers = {"Context-Type": "text/json", "Authorization": f"Bearer {api_token}"}

        response = request_lib.post(url=f"{api_url}/api/2.0/serving-endpoints", json=data, headers=headers, timeout=60)
        print("Deployed endpoint.. Response status:", response.status_code)
        print("Deployed endpoint.. Response text:", response.text, "\n")
        return production_model

    def _log_model(self, model_wrapper: ModelWrapper):
        custom_model = model_wrapper.custom_model
        run_id = model_wrapper.run_id
        registered_model_name = get_registered_model_name(run_id)
        model_wrapper.registered_model_name = registered_model_name
        with start_run(experiment_id=self.experiment_id, run_id=run_id):
            mlflow.pyfunc.log_model(
                "model",
                python_model=custom_model,
                pip_requirements=["pandas", "mlflow", f"databricks-genai=={__version__}", "databricks-connect"],
                signature=custom_model.signature,
                registered_model_name=registered_model_name)

    def _get_exp_id(self, experiment_name: str):
        experiment = get_experiment_by_name(experiment_name)
        if not experiment:
            print(f"Experiment {experiment_name} not found. Creating new experiment...")
            return create_experiment(name=experiment_name)

        print(f"Experiment {experiment_name} found. Using existing experiment...")
        return experiment.experiment_id

    def _create_custom_metrics(self):
        """Create custom metrics for the model.

        Generates custom metrics for the model based on the self.current_task_spec.eval_criteria.
        Assumes that self.evaluation_criteria is already set.(i.e. compile() has been called)
        """

        def _wrapper_fn(request: str, response: str, guideline: str, metric_name: str):
            assessment = judges.guideline_adherence(
                request=request,
                response=response,
                guidelines=[guideline],
            )
            return Assessment(name=metric_name,
                              value=assessment.value,
                              rationale=assessment.rationale,
                              source=assessment.source)

        eval_criteria = self.current_task_spec.evaluation_criteria
        assert eval_criteria
        self.custom_metrics = []
        for criterion in eval_criteria:
            metric_name = re.sub(r'[^a-zA-Z0-9]', '_', criterion)
            custom_metric_fn = functools.partial(_wrapper_fn, guideline=criterion, metric_name=metric_name)
            custom_metric = metric(eval_fn=custom_metric_fn, name=metric_name)
            self.custom_metrics.append(custom_metric)

    def _create_classic_metrics(self):
        """Creates classic metrics for given the instruction type. 

        classic metrics are created based on the instruction type and includes 
        metrics such as fuzzy match & exact match.

        NOTE: Assumes self.current_params.instruction_info is already set.
        """
        assert self.current_params.instruction_info.instruction_type
        classic_metrics = create_classic_metrics(self.current_params.instruction_info.instruction_type)
        self.custom_metrics.extend(classic_metrics)

    def create_models(self):
        self.model_map.clear()
        model_list = create_t2t_model_list(self.current_params)
        for model_config in model_list:
            model = self._create_text2text_model(model_config)
            self.model_map[model.run_name] = model
            if model_config.is_default:
                self.default_model = model
            self._log_model(model)

    def _create_text2text_model(self, model_config: T2TModelConfig) -> ModelWrapper:
        with start_run(
                experiment_id=self.experiment_id,
                description=model_config.name,
        ) as run:
            signature = infer_signature(model_input=["input"], model_output=["output"])
            custom_model = CustomModel(
                model_config.model,
                signature,
                model_config.name,
            )
            run_id = run.info.run_id
            run_name = run.info.run_name
            return ModelWrapper(custom_model, run_id, run_name, registered_model_name=None)

    def _get_model_predictions(self,
                               model_wrapper: ModelWrapper,
                               requests: List[str],
                               with_traces: bool = False,
                               max_workers: int = _MODEL_CONCURRENCY) -> List[PredictionResult]:
        """Get predictions from model in parallel.

        Args:
            model_wrapper: ModelWrapper containing the model and metadata
            requests: List of requests to process
            with_traces: Whether to capture MLflow traces
            max_workers: Number of parallel workers

        Returns:
            List of PredictionResults containing predictions and optional traces
        """

        def predict_single(req: str) -> PredictionResult:
            if not with_traces:
                return PredictionResult(model_wrapper.custom_model.predict(None, req))

            root_span = self.mlflow_client.start_trace(name=model_wrapper.run_name)
            prediction = model_wrapper.custom_model.predict(None, req)
            self.mlflow_client.end_trace(root_span.request_id)
            return PredictionResult(prediction=prediction, trace=get_trace(root_span.request_id).to_json())

        desc = f"{'Evaluating' if with_traces else 'Visualizing'} model {model_wrapper.run_name}"
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(tqdm(executor.map(predict_single, requests), total=len(requests), desc=desc))

    def _visualize_model(self, model_wrapper: ModelWrapper, data: Optional[List[Dict[str, str]]] = None):
        eval_data = data or [{
            'request': datum[0],
            'response': datum[1]
        } for datum in self.current_params.labelled_test_examples[0:self.MAX_EXAMPLES_FOR_VISUALIZATION]]
        requests = [datum['request'] for datum in eval_data]

        results = self._get_model_predictions(model_wrapper, requests)

        return [{
            "input": datum['request'],
            "model_output": result.prediction,
            **({
                "label": datum['response']
            } if 'response' in datum else {})
        } for datum, result in zip(eval_data, results)]

    def _evaluate_model(self,
                        model_wrapper: ModelWrapper,
                        data: Optional[List[Dict[str, str]]] = None) -> mlflow.models.EvaluationResult:
        eval_data = data or [{
            'request': datum[0],
            'response': datum[1]
        } for datum in self.current_params.labelled_test_examples[0:self.MAX_EVAL_DATA]]

        if not self.current_params.evaluation_criteria:
            raise ValueError("Evaluation criteria is not provided. Please invoke `compile()` API.")

        requests = [
            INSTRUCTION_AND_INPUT_PROMPT_TEMPLATE.format(instruction=self.current_params.instruction,
                                                         inp=datum['request']) for datum in eval_data
        ]

        with start_run(experiment_id=self.experiment_id, run_id=model_wrapper.run_id):
            results = self._get_model_predictions(model_wrapper, requests, with_traces=True)

            eval_df = pd.DataFrame({
                "request": requests,
                "expected_response": [datum['response'] for datum in eval_data],
                "response": [r.prediction for r in results],
                "trace": [r.trace for r in results]
            })

            return mlflow.evaluate(
                data=eval_df,
                model_type="databricks-agent",  # Enable Mosaic AI Agent Evaluation
                extra_metrics=self.custom_metrics,
                # Disable built-in judges.
                evaluator_config={'databricks-agent': {
                    "metrics": [],
                }})
