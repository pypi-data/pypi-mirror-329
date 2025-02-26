"""Script used to upload the KIE grounding model to model registry."""

import argparse
import logging
import os
import shutil

import mlflow
from databricks.sdk.core import Config
from mlflow.models.signature import ModelSignature, ParamSchema
from mlflow.types.schema import ColSpec, ParamSpec, Schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mlflow.set_tracking_uri("databricks")
mlflow.set_registry_uri("databricks-uc")


def save_model(local_output_path="grounding_model"):
    """Save the KIE grounding model with artifacts."""
    # pylint: disable=import-outside-toplevel
    from kie_grounding_model import KIEGroundingModel

    model = KIEGroundingModel()

    input_schema = Schema([ColSpec("string", "request"), ColSpec("string", "expected_response", required=False)])
    output_schema = Schema([
        ColSpec("string", "request"),
        ColSpec("string", "expected_response", required=False),
        ColSpec("string", "generated_response"),
        ColSpec("string", "eval_results"),
    ])
    params_schema = ParamSchema([ParamSpec("json_schema", "string", None)])
    signature = ModelSignature(inputs=input_schema, outputs=output_schema, params=params_schema)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    kie_grounding_model_path = os.path.join(current_dir, "kie_grounding_model.py")

    mlflow.pyfunc.save_model(path=local_output_path,
                             python_model=model,
                             signature=signature,
                             code_paths=[kie_grounding_model_path],
                             pip_requirements=[
                                 'pandas>=1.5.0',
                                 'requests>=2.28.0',
                                 'mlflow>=2.8.0',
                                 'databricks-connect>=13.0',
                                 'pydantic>=2.0.0',
                                 'databricks-genai==1.2.0a14',
                             ])


def upload(model_registry_path: str, local_output_path: str = "grounding_model", profile: str = "DEFAULT"):
    """Upload the KIE grounding model to the staging registry.
    
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

        logger.info(
            f"Registering grounding model to the workspace {config.host} at model registry path {model_registry_path}")
        mlflow.register_model(model_uri=local_output_path, name=model_registry_path)
        logger.info(f"Registered model to {model_registry_path}")

    except (ImportError, mlflow.exceptions.MlflowException) as e:
        logger.error(f"Failed to register model: {e}")
    finally:
        if os.path.exists(local_output_path) and os.path.isdir(local_output_path):
            shutil.rmtree(local_output_path)
            logger.info(f"Deleted existing model at {local_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload KIE grounding model")
    parser.add_argument("--model_registry_path",
                        type=str,
                        required=True,
                        help="Path in the model registry to upload the grounding model to")
    parser.add_argument("--profile", type=str, default="DEFAULT", help="Profile to use from ~/.databrickscfg")
    parser.add_argument("--local_output_path",
                        default="grounding_model",
                        type=str,
                        help="Path to save the model locally")
    args = parser.parse_args()

    upload(model_registry_path=args.model_registry_path, local_output_path=args.local_output_path, profile=args.profile)
