"""Utility functions for abstract out request construction / response parsing of Text-to-Text tasks."""

import json
import re
from typing import Dict, List, Optional, Tuple

from databricks.sdk import WorkspaceClient  # pylint: disable = ungrouped-imports
from databricks.sdk.errors import ResourceDoesNotExist  # pylint: disable = ungrouped-imports
from openai.lib._parsing._completions import type_to_response_format_param
from pydantic import BaseModel, Field, create_model

from databricks.kie.inference_utils import get_llm_proxy_chat_completion_response
from databricks.model_training.mlflow_utils import get_default_model_registry_path_info

INSTRUCTION_AND_INPUT_PROMPT_TEMPLATE = """## User input : {inp}

## Instruction : {instruction}
"""

SYSTEM_PROMPT_TEMPLATE = """
You are a helpful AI Agent. Please follow the following instructions with given input.
The instruction provided by the user is included following the "Instruction" header below.
The instruction describes the general task that the user would like to accomplish.

Instruction : '{instruction}'

The specific input for this request is included in the as part of user message.
"""

USER_PROMPT_TEMPLATE = """
user input : '{inp}'
"""

CHAIN_OF_THOUGHT_SYSTEM_PROMPT = """
Given instruction and user input provided as the system message and user messages above, generate CoT class.

CoT class provide a detailed step-by-step reasoning that leads to answering the provided user instruction.
CoT class has 2 fields: `step_by_step_reasoning` and `concise_response`.

step_by_step_reasoning : please provide detailed step-by-step reasoning that leads to answering the provided user instruction.
concise_response: please provide the most correct and concise answer to the user instruction.

If few shot examples are provided in the user messages above, refer to assistant messages in few shot examples
to infer the `concise_response` fields. Note that previous assistant output to few shot examples does not
include the `step_by_step_reasoning`. If few shot examples exists as messages above, refer to them as
examples for generating the `concise_response` field. Always generate the `step_by_step_reasoning` field first
and then generate the `concise_response` field.
"""

EXPERIMENT_NAME_GENERATION_PROMPT = """
You are a helpful AI Agent. Given user instruction, please generate a name of an experiment from the instruction.

## Task
You goal is to generate a name of an experiment from the user instruction.

## Output
You should output the name of an experiment as a string.
- Name should be in snake_case format.
- Name should be concise and to the point.
- Name should be no more than 10 words and should not exeed one sentence.
- Name should not contain any special characters, only alphanumeric and underscores are allowed.
"""


class CoT(BaseModel):
    step_by_step_reasoning: str = Field(
        description="Detailed step by step reasoning that leads to answering the provided user instruction.")
    concise_response: str = Field(description="The most correct and concise answer to the user instruction.")


def create_chat_completions_request(messages: List[Dict[str, str]], response_format: Optional[Dict] = None):
    """
    Creates a chat completions request json.

    Args:
        messages (list): A list of message dictionaries to be included in the request.
        response_format (str, optional): The desired format of the response. Defaults to None.

    Returns:
        dict: A dictionary representing the chat completions request.
    """
    chat_completion_req: Dict = {
        "messages": messages,
    }
    if response_format:
        chat_completion_req['response_format'] = response_format
    return chat_completion_req


def create_chat_completions_messages_from_instruction(instruction: str,
                                                      inp: str,
                                                      few_shot_examples: Optional[List[Tuple[str, str]]] = None):
    """
    Creates a list of chat completion messages based on the given instruction and input.

    Args:
        instruction (str): The instruction to be included in the system message.
        inp (str): The input to be included in the user message.
        few_shot_examples (list, optional): A list of tuples containing ground truth request and response pairs.
    Returns:
        list: A list of dictionaries representing the chat messages. Each dictionary contains
              a 'role' key (either 'system' or 'user') and a 'content' key with the respective message.
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(instruction=instruction)}]
    if few_shot_examples:
        for example_input, example_output in few_shot_examples:
            messages.append({"role": "user", "content": USER_PROMPT_TEMPLATE.format(inp=example_input)})
            messages.append({"role": "assistant", "content": example_output})

    messages += [{"role": "user", "content": USER_PROMPT_TEMPLATE.format(inp=inp)}]
    return messages


def generate_cot_response(model_id: str, messages: List[Dict], temperature: Optional[float] = None) -> str:
    """
    Generates a response that has gone through CoT reasoning.

    Note: CHAIN of thought reasoning is not returned -- it is used only for improving reasoning
    as model autoregressively generates the response tokens.
    The implementation is structured such that chain of thought reasoning is always generated first.

    Args:
        model_id (str): The model identifier to use for generating the response.
        messages (list): A list of message dictionaries to be included in the request.
            Corresponds to chat completion messges.
        temperature (Optional[float]): The temperature for sampling from the model.

    Returns:
        str: The most correct and concise answer to the user instruction
    """
    messages.append({"role": "system", "content": CHAIN_OF_THOUGHT_SYSTEM_PROMPT})
    req = create_chat_completions_request(messages, type_to_response_format_param(CoT))
    res = get_llm_proxy_chat_completion_response(model_id, req, temperature=temperature)
    cot_response = CoT(**json.loads(res))
    return cot_response.concise_response


def generate_exp_name_from_instruction(instruction: str) -> str:
    """Generates an experiment name from an instruction.

    Args:
        instruction (str): The instruction to generate the experiment name from.

    Returns:
        str: The experiment name.
    """
    messages = create_chat_completions_messages_from_instruction(instruction=EXPERIMENT_NAME_GENERATION_PROMPT,
                                                                 inp=instruction)
    req = create_chat_completions_request(messages)
    res = get_llm_proxy_chat_completion_response("gpt-4o-mini-2024-07-18-text2text", req)
    return re.sub(r'[^a-zA-Z0-9]', '_', res)


def get_registered_model_name(run_id: str) -> str:
    """
    Returns the registered model name for the given run id.

    Args:
        run_id (str): The run id to get the registered model name for.

    Returns:
        str: The registered model name.
    """
    catalog, schema = get_default_model_registry_path_info()
    return f"{catalog}.{schema}.{run_id}"


def create_structured_outputs_using_cot(clz: BaseModel,
                                        messages: List[Dict],
                                        model_id: Optional[str] = "gpt-4o-2024-08-06-text2text") -> BaseModel:
    """
    Creates a structured output using CoT reasoning.

    Args:
        clz (BaseModel): The pydantic base class generated.
        messages (list): A list of message dictionaries to be included in the request.
            May include examples as form of user messages and assistant messages. If few shot examples
            are provided, they should be included as user messages and assistant messages, and the assistant
            messages content should be the `json.dumps` of the pydantic class.
        model_id (str): The model identifier to use for generating the response.

    Raises:
        ValueError: If any assistant message content (provided as few shot examples) is not valid JSON
            or does not match the target schema.

    Returns:
        BaseModel: The structured output instance of the pydantic model generated using CoT reasoning.
    """
    dynamic_model_clz = create_model(
        'CoT',
        step_by_step_reasoning=(
            str,
            Field(
                description="Detailed step-by-step reasoning that leads to answering the provided user instruction.")),
        concise_response=(clz, Field(description="The most correct and concise answer to the user instruction.")))

    # Verify that all assistant messages (ICL examples) contain valid JSON that can be parsed by the target class
    for message in messages:
        if message['role'] == 'assistant':
            try:
                content = json.loads(message['content'])
                clz(**content)  # Validate content matches expected schema
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError("Assistant message content must be valid JSON matching the target schema "
                                 f"for class {clz.__name__}. Error: {str(e)}") from e

    messages.append({"role": "system", "content": CHAIN_OF_THOUGHT_SYSTEM_PROMPT})
    req = create_chat_completions_request(messages, type_to_response_format_param(dynamic_model_clz))
    res = get_llm_proxy_chat_completion_response(model_id, req)
    output = json.loads(res)
    cot_response = dynamic_model_clz(**output)
    return cot_response.concise_response


def validate_secret_exists(secret_scope: str, secret_key: str) -> bool:
    """
    Validates if the secret exists in the secret scope.

    Args:
        secret_scope (str): The secret scope name.
        secret_key (str): The secret key name.

    Returns:
        bool: True if the secret exists, False otherwise.
    """
    w = WorkspaceClient()
    try:
        w.secrets.get_secret(scope=secret_scope, key=secret_key)
        return True
    except ResourceDoesNotExist:
        return False
