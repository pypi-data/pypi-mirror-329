"""Utils for working with model serving"""

from typing import NamedTuple, Optional

from mlflow import MlflowClient

MODEL_CONTEXT_LENGTH = 131072


class ModelSpecs(NamedTuple):
    name: str
    endpoint: Optional[str]
    cost_per_hour: float  # This is measured in DBUs instead of dollars, since customers may have different DBU rates
    ft_model_name: str
    is_hosted: bool = True
    uc_schema: Optional[str] = None
    version: Optional[str] = None
    cost_per_m_ft_tokens: Optional[float] = None
    alias: Optional[str] = None


def get_latest_model_version(model_name: str) -> str:
    """Get the latest version of a model using Mlflow

    Args:
        model_name (str): The name of the model

    Returns:
        str: The latest version of the model
    """
    client = MlflowClient()
    model_versions = client.search_model_versions(f"name='{model_name}'")

    if not model_versions:
        raise ValueError(f"No model versions found for model '{model_name}'")

    version_numbers = [int(model.version) for model in model_versions]
    most_recent_version = max(version_numbers)
    return str(most_recent_version)


def get_model_by_ft_name(ft_model_name: str) -> Optional[str]:
    model_specs = get_model_specs()
    for model_spec in model_specs.values():
        if model_spec.ft_model_name == ft_model_name:
            return model_spec.name


pt_dbu_cost_per_hour = {
    # from https://www.databricks.com/product/pricing/foundation-model-serving
    'databricks-meta-llama-3-3-70b-instruct': 342.857,
    'databricks-meta-llama-3-1-8b-instruct': 106,
    'databricks-meta-llama-3-2-3b-instruct': 92.857,
}


def get_model_specs():
    model_specs = {
        'balanced':
            ModelSpecs("balanced",
                       endpoint='databricks-meta-llama-3-3-70b-instruct',
                       cost_per_hour=pt_dbu_cost_per_hour['databricks-meta-llama-3-3-70b-instruct'],
                       ft_model_name='meta-llama/Llama-3.3-70B-Instruct',
                       uc_schema='system.ai.llama_v3_3_70b_instruct',
                       version=get_latest_model_version('system.ai.llama_v3_3_70b_instruct'),
                       alias='elephant'),
        'cost-optimized-medium':
            ModelSpecs("cost-optimized-medium",
                       endpoint='databricks-meta-llama-3-1-8b-instruct',
                       cost_per_hour=pt_dbu_cost_per_hour['databricks-meta-llama-3-1-8b-instruct'],
                       ft_model_name='meta-llama/Meta-Llama-3.1-8B-Instruct',
                       is_hosted=False,
                       uc_schema='system.ai.meta_llama_v3_1_8b_instruct',
                       version=get_latest_model_version('system.ai.meta_llama_v3_1_8b_instruct'),
                       cost_per_m_ft_tokens=4,
                       alias='zebra'),
        'cost-optimized-small':
            ModelSpecs("cost-optimized-small",
                       endpoint=None,
                       cost_per_hour=pt_dbu_cost_per_hour['databricks-meta-llama-3-2-3b-instruct'],
                       ft_model_name='meta-llama/Llama-3.2-3B-Instruct',
                       is_hosted=False,
                       uc_schema='system.ai.llama_v3_2_3b_instruct',
                       version=get_latest_model_version('system.ai.llama_v3_2_3b_instruct'),
                       cost_per_m_ft_tokens=2.50,
                       alias='squirrel'),
    }
    return model_specs
