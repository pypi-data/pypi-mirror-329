"""Module to encapsulate LLM invocation logic as custom MLFLow PythonModel."""

from typing import Dict, Optional

import mlflow
from mlflow.models import ModelSignature
from mlflow.pyfunc import PythonModelContext

from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel


class CustomModel(mlflow.pyfunc.PythonModel):
    """
    A custom MLflow Python model that processes inputs based on provided instructions.

    Args:
        model (BaseT2TModel): The model to use for generating predictions.
        signature (ModelSignature): The signature of the model.
        model_descriptor (str): The descriptor of the model.
    """

    def __init__(self, model: BaseT2TModel, signature: ModelSignature, model_descriptor: str = None):
        self.model = model
        self.model_descriptor = model_descriptor
        self.signature = signature

    def predict(self, context: PythonModelContext, model_input: str, params: Optional[Dict] = None):
        del context, params
        return self.model(model_input)


class ModelWrapper():

    def __init__(self,
                 custom_model: CustomModel,
                 model_run_id: str,
                 run_name: str,
                 registered_model_name: Optional[str] = None):
        self.custom_model = custom_model
        self.run_id = model_run_id
        self.run_name = run_name
        self.registered_model_name = registered_model_name

    def get_model_path(self):
        return f"runs:/{self.run_id}/model"
