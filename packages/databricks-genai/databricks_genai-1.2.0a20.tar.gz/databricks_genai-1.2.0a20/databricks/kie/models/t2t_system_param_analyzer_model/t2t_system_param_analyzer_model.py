"""Pyfunc model abstraction for T2T system parameter recommendation."""

import json
import logging
from dataclasses import is_dataclass
from typing import Any, Dict

import mlflow
import pandas as pd
from mlflow.pyfunc import PythonModel
from pydantic import BaseModel

from databricks.kie.t2t_evaluation_criteria_generator import (add_evaluation_criteria_from_preference_data,
                                                              generate_evaluation_criteria)
from databricks.kie.t2t_instruction_analyzer import populate_instruction_info
from databricks.kie.t2t_schema import PreferenceData, T2TSystemParams

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO(jun.choi): Include this as part of SDK t2t_utils.py instead.
def custom_asdict(obj):
    """Convert a dataclass or pydantic object to a dictionary."""
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, list):
        return [custom_asdict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: custom_asdict(v) for k, v in obj.items()}
    elif is_dataclass(obj):
        return {field.name: custom_asdict(getattr(obj, field.name)) for field in obj.__dataclass_fields__.values()}
    else:
        return obj


class T2TSystemParamAnalyzerModel(PythonModel):
    """MLflow model for T2T system parameter analyzer."""

    def load_context(self, context) -> None:
        """Load the model artifacts from the context."""
        mlflow.set_tracking_uri("databricks")
        mlflow.set_registry_uri("databricks-uc")

    def predict(self, context, model_input: pd.DataFrame, params: Dict[str, Any] = None):
        """Label T2T grounding samples and return evaluation results.
        Args:
            context: MLflow context
            model_input: DataFrame with `request`, `rejected_output`, `preferred_output` columns.
            params: Dictionary with `current_task_spec` key.

        Returns:
            Dictionary containing details on a new T2T system parameters after grounding.
        """
        del context

        if params is None or 'current_task_spec' not in params:
            raise ValueError("Expected params to be a dict containing the 'current_task_spec' key.")

        # check that `model_input` has all required columns
        if not all(col in model_input.columns for col in ['request', 'rejected_output', 'preferred_output']):
            raise ValueError("model_input should have 'request', 'rejected_output', 'preferred_output' columns.")

        preference_data = []
        for request, rejected_output, preferred_output in model_input[[
                'request', 'rejected_output', 'preferred_output'
        ]].itertuples():
            preference_data.append(
                PreferenceData(input=request, rejected_response=rejected_output, preferred_response=preferred_output))

        current_task_spec_str = params['current_task_spec']
        try:
            task_spec_json = json.loads(current_task_spec_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse 'current_task_spec': {e}") from e

        current_task_spec = T2TSystemParams(**task_spec_json)
        # TODO(jun.choi): Use diff between previous and current task spec.
        # previous_task_spec = T2TSystemParams(**params['previous_task_spec'])
        if not current_task_spec.evaluation_criteria:
            inferred_eval_criteria = generate_evaluation_criteria(current_task_spec.instruction,
                                                                  current_task_spec.labelled_test_examples)
            current_task_spec.evaluation_criteria = inferred_eval_criteria

        # If user provided labels or corrections, then add them to the evaluation criteria.
        if preference_data:
            new_eval_criteria = add_evaluation_criteria_from_preference_data(
                current_task_spec.instruction,
                current_task_spec.evaluation_criteria,
                preference_data,
            )
            current_task_spec.evaluation_criteria = new_eval_criteria

        populate_instruction_info(current_task_spec)
        return {"task_spec": custom_asdict(current_task_spec)}
