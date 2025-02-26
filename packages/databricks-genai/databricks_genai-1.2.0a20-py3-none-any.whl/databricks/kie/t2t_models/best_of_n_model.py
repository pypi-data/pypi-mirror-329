"""Model that selects the best response from a set of responses based on a value model."""
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional

from databricks.kie.research_common.reward_models import ContextRewardModel, RewardModel, make_reward_model
from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_models.t2t_model_registry import model_registry
from databricks.kie.t2t_schema import T2TSystemParams

DEFAULT_BEST_OF_N = 8
DEFAULT_INNER_MODEL_NAME = "t2t_baseline_model"


class BestOfNModel(BaseT2TModel):
    """Model that selects the best response from a set of responses based on a value model."""

    def __init__(self, inner_model: BaseT2TModel, reward_model: RewardModel, best_of_n: int = DEFAULT_BEST_OF_N):
        self.inner_model = inner_model
        self.reward_model = reward_model
        self.best_of_n = best_of_n

    @staticmethod
    def create_from_system_param(system_param: T2TSystemParams, **kwargs) -> Optional[BaseT2TModel]:
        best_of_n = kwargs.pop("best_of_n", DEFAULT_BEST_OF_N)
        value_model_name = kwargs.pop("value_model_name", "context")
        value_model_params = kwargs.pop("value_model_params", {})
        inner_model_name = kwargs.pop("inner_model_name", DEFAULT_INNER_MODEL_NAME)

        reward_model = make_reward_model(value_model_name, **value_model_params)
        inner_model_constructor: Callable[[T2TSystemParams], BaseT2TModel] = model_registry.get(inner_model_name)
        inner_model = inner_model_constructor(system_param, **kwargs)
        return BestOfNModel(inner_model=inner_model, reward_model=reward_model, best_of_n=best_of_n)

    def __call__(self, model_input: str) -> str:
        return select_best_response(self.inner_model, model_input, self.reward_model, self.best_of_n)


def select_best_response(model: BaseT2TModel,
                         prompt: str,
                         reward_model: Optional[RewardModel] = None,
                         n: int = DEFAULT_BEST_OF_N) -> str:
    if reward_model is None:
        reward_model = ContextRewardModel()
    results = []
    values = []

    # parallelize this
    def get_result_and_value(_):
        result = model(prompt)
        value = reward_model(prompt, result)
        return result, value

    with ThreadPoolExecutor(max_workers=DEFAULT_BEST_OF_N) as executor:
        results_and_values = executor.map(get_result_and_value, range(n))

    results, values = zip(*results_and_values)

    return max(zip(results, values), key=lambda x: x[1])[0]
