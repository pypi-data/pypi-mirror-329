"""Baseline text-to-text model that uses templated instruction only."""
from typing import Any, Optional

from databricks.kie.inference_utils import get_llm_proxy_chat_completion_response
from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_models.t2t_model_registry import model_registry
from databricks.kie.t2t_schema import T2TSystemParams
from databricks.kie.t2t_utils import create_chat_completions_messages_from_instruction, create_chat_completions_request


@model_registry("t2t_baseline_model", is_default=False)
class T2TBaselineModel(BaseT2TModel):
    """A baseline text-to-text model that uses templated instruction only.

    Args:
        instruction (str): The instruction guiding the model's behavior.
        temperature (Optional[float]): The temperature for sampling from the model.
    """
    DEFAULT_MODEL_ID = "gpt-4o-mini-2024-07-18-text2text"

    def __init__(self, instruction: str, temperature: Optional[float] = None):
        self.instruction = instruction
        self.temperature = temperature

    def __call__(self, model_input: str) -> str:
        messages = create_chat_completions_messages_from_instruction(instruction=self.instruction, inp=model_input)
        req = create_chat_completions_request(messages)
        return get_llm_proxy_chat_completion_response(self.DEFAULT_MODEL_ID, req, self.temperature)

    @staticmethod
    def create_from_system_param(system_param: T2TSystemParams, **kwargs: Any) -> Optional['T2TBaselineModel']:
        instruction = system_param.instruction
        return T2TBaselineModel(instruction=instruction, temperature=kwargs.get("temperature", None))
