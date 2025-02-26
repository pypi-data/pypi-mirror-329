"""Script used to upload the T2T system parameter analyzer model to model registry."""

import argparse
import logging
import os
import shutil

import mlflow
from databricks.sdk.core import Config
from mlflow.models.signature import ModelSignature, ParamSchema
from mlflow.types.schema import ColSpec, ParamSpec, Schema
from t2t_system_param_analyzer_model import T2TSystemParamAnalyzerModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mlflow.set_tracking_uri("databricks")
mlflow.set_registry_uri("databricks-uc")


def save_model(local_output_path="t2t_system_param_analyzer_model"):
    """Save the T2T system parameter analyzer model with artifacts."""
    model = T2TSystemParamAnalyzerModel()

    input_schema = Schema([
        ColSpec("string", "request"),
        ColSpec("string", "rejected_output", required=False),
        ColSpec("string", "preferred_output", required=False)
    ])
    # TODO(jun.choi): Correctly specify schema as nested dictionary.
    output_schema = Schema([
        ColSpec("string", "new_task_spec"),
    ])
    params_schema = ParamSchema([
        ParamSpec("current_task_spec", "string", None),
    ])
    signature = ModelSignature(inputs=input_schema, outputs=output_schema, params=params_schema)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    t2t_system_param_analyzer_model_path = os.path.join(current_dir, "t2t_system_param_analyzer_model.py")

    mlflow.pyfunc.save_model(path=local_output_path,
                             python_model=model,
                             signature=signature,
                             code_paths=[t2t_system_param_analyzer_model_path],
                             pip_requirements=[
                                 'databricks-connect>=13.0',
                                 'databricks-genai==1.2.0a19',
                             ])


def upload(model_registry_path: str,
           local_output_path: str = "t2t_system_param_analyzer_model",
           profile: str = "DEFAULT"):
    """Upload the T2T system parameter analyzer model to the staging registry.
    Args:
        model_registry_path: Path in the model registry to upload the model to
        local_output_path: Local path to save the model artifacts
        profile: Profile to use from ~/.databrickscfg
    """
    config = Config(profile=profile)
    os.environ["DATABRICKS_HOST"] = config.host
    os.environ["DATABRICKS_TOKEN"] = config.token

    try:
        save_model(local_output_path)

        logger.info(f"Registering system parameter analyzer model to the workspace {config.host}"
                    f" at model registry path {model_registry_path}")
        mlflow.register_model(model_uri=local_output_path, name=model_registry_path)
        logger.info(f"Registered model to {model_registry_path}")

    except (ImportError, mlflow.exceptions.MlflowException) as e:
        logger.error(f"Failed to register model: {e}")
    finally:
        if os.path.exists(local_output_path) and os.path.isdir(local_output_path):
            shutil.rmtree(local_output_path)
            logger.info(f"Deleted existing model at {local_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload T2T system parameter analyzer model")
    parser.add_argument("--model_registry_path",
                        type=str,
                        required=True,
                        help="Path in the model registry to upload the system parameter analyzer model to")
    parser.add_argument("--profile", type=str, default="DEFAULT", help="Profile to use from ~/.databrickscfg")
    parser.add_argument("--local_output_path",
                        default="t2t_system_param_analyzer_model",
                        type=str,
                        help="Path to save the model locally")
    args = parser.parse_args()

    upload(model_registry_path=args.model_registry_path, local_output_path=args.local_output_path, profile=args.profile)
