"""Text2Text model that uses prompt tuning technique."""

import random
from typing import List, Optional, Tuple

from databricks.kie.inference_utils import get_llm_proxy_chat_completion_response
from databricks.kie.t2t_models.base_t2t_model import BaseT2TModel
from databricks.kie.t2t_schema import InstructionInfo, T2TSystemParams
from databricks.kie.t2t_utils import (create_chat_completions_messages_from_instruction,
                                      create_chat_completions_request, generate_cot_response)

MODEL_SELECTION_WITH_STRUCTURED_OUTPUT_SUPPORT = ["gpt-4o-2024-08-06-text2text", "gpt-4o-mini-2024-07-18-text2text"]


class T2TPromptTuningModel(BaseT2TModel):
    """A text-to-text model that uses prompt tuning with an underlying LLM.

    Args:
        instruction (str): The instruction guiding the model's behavior.
        model_id (str): The identifier of the underlying language model to use for generating predictions.
        few_shot_examples (Optional[List[Dict[str, str]]]): A list of few-shot examples for model signature inference.
        instruction_info (Optional[InstructionInfo]): The instruction info for the model.
        use_cot (bool): Whether to use chain-of-thought (CoT) for reasoning.
        temperature (Optional[float]): The temperature for sampling from the model.
    """
    INSTRUCTION_TEMPLATE = """
        INSTRUCTION: {optimized_instruction}
        OUTPUT FORMAT: {output_format}

        Given the following instruction and output format, provide response that follows the instruction and output format given the user input.
        User input will be provided below as part of the user message.  
    """
    MAX_ICL_EXAMPLES = 8

    def __init__(self,
                 instruction: str,
                 model_id: str,
                 few_shot_examples: Optional[List[Tuple[str, str]]] = None,
                 instruction_info: Optional[InstructionInfo] = None,
                 use_cot: bool = False,
                 temperature: Optional[float] = None):
        random.seed(0)
        self.instruction = instruction
        self.instruction_info = instruction_info
        self.model_id = model_id
        self.few_shot_examples = few_shot_examples or []
        self.temperature = temperature
        if len(self.few_shot_examples) > self.MAX_ICL_EXAMPLES:
            self.few_shot_examples = random.sample(self.few_shot_examples, self.MAX_ICL_EXAMPLES)

        self.use_cot = use_cot

    def __call__(self, model_input: str) -> str:
        instruction = self._get_instruction()
        messages = create_chat_completions_messages_from_instruction(instruction=instruction,
                                                                     inp=model_input,
                                                                     few_shot_examples=self.few_shot_examples)
        if self.use_cot:
            return generate_cot_response(self.model_id, messages, temperature=self.temperature)

        req = create_chat_completions_request(messages)
        return get_llm_proxy_chat_completion_response(self.model_id, req, temperature=self.temperature)

    def _get_instruction(self) -> str:
        if not self.instruction_info:
            return self.instruction

        optimized_instruction = self.instruction_info.optimized_instruction
        output_format = self.instruction_info.output_format
        return self.INSTRUCTION_TEMPLATE.format(optimized_instruction=optimized_instruction,
                                                output_format=output_format)

    @staticmethod
    def create_from_system_param(system_param: T2TSystemParams,
                                 use_cot: bool,
                                 model_id: str,
                                 temperature: Optional[float] = None) -> Optional['T2TPromptTuningModel']:
        if use_cot and model_id not in MODEL_SELECTION_WITH_STRUCTURED_OUTPUT_SUPPORT:
            return None

        instruction = (system_param.instruction_info.optimized_instruction
                       if system_param.instruction_info else system_param.instruction)
        few_shot_examples = system_param.labelled_training_examples
        return T2TPromptTuningModel(instruction=instruction,
                                    instruction_info=system_param.instruction_info,
                                    few_shot_examples=few_shot_examples,
                                    use_cot=use_cot,
                                    model_id=model_id,
                                    temperature=temperature)
