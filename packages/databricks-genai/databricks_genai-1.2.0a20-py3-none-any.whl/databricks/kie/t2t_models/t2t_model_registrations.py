"""Registry for T2T models."""

import functools
from typing import List

from databricks.kie.t2t_models.all_t2t_models import *  # pylint: disable=wildcard-import,unused-wildcard-import
from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_models.t2t_model_registry import T2TModelConfig, model_registry
from databricks.kie.t2t_schema import T2TSystemParams


def create_t2t_model_list(task_spec: T2TSystemParams) -> List[T2TModelConfig]:
    """Create a list of T2TModelConfig objects from the registry given a task spec."""
    models = []
    for name, func in model_registry.get_all().items():
        model = func(task_spec)
        if model is None:
            continue

        is_default = model_registry.default_model and name == model_registry.default_model.name
        models.append(T2TModelConfig(name=name, is_default=is_default, model=model))
    return models


def get_t2t_default_model(task_spec: T2TSystemParams) -> BaseT2TModel:
    """Get the default model from the registry.

    Args: 
        task_spec: T2TSystemParams to create the default model

    Returns:
        Default model constructed from provided task_spec.

    Raises:
        ValueError: If no default model is registered
    """
    if model_registry.default_model is None:
        raise ValueError("No default model registered")

    return model_registry.default_model.factory(task_spec)


################################################################################
# Manually add models to T2T Model Registry
#
# NOTE: Class can be added using decorators.
################################################################################
model_registry.register("prompt_tuning_model_gpt_4o_cot",
                        to_register=functools.partial(T2TPromptTuningModel.create_from_system_param,
                                                      model_id="gpt-4o-2024-08-06-text2text",
                                                      use_cot=True),
                        is_default=True)
model_registry.register("prompt_tuning_model_gpt_4o",
                        to_register=functools.partial(T2TPromptTuningModel.create_from_system_param,
                                                      model_id="gpt-4o-2024-08-06-text2text",
                                                      use_cot=False),
                        is_default=False)
model_registry.register("prompt_tuning_model_gpt_4o_mini_cot",
                        to_register=functools.partial(T2TPromptTuningModel.create_from_system_param,
                                                      model_id="gpt-4o-mini-2024-07-18-text2text",
                                                      use_cot=True),
                        is_default=False)
model_registry.register("prompt_tuning_model_gpt_4o_mini",
                        to_register=functools.partial(T2TPromptTuningModel.create_from_system_param,
                                                      model_id="gpt-4o-mini-2024-07-18-text2text",
                                                      use_cot=False),
                        is_default=False)
model_registry.register("best_of_n_model_gpt_4o_mini_cot",
                        to_register=functools.partial(
                            BestOfNModel.create_from_system_param,
                            inner_model_name="prompt_tuning_model_gpt_4o_mini_cot",
                            temperature=1.,
                        ),
                        is_default=False)
