"""Module that encapsulates instruction analysis for Text2Text."""

from databricks.kie.inference_utils import generate_base_model_using_chat_completion_messages
from databricks.kie.t2t_schema import InstructionInfo, InstructionType, T2TSystemParams

INSTRUCTION_INFO_GENERATION_WITHOUT_ICL = """
You are an expert in instruction analysis and generation. That is, given 
- the original instruction provided by the user
- List of criteria that response should satisfy
you should `infer` the OPTIMAL instruction to generate the response given the request. Instruction should be as detailed as possible.

The instruction info to generate has the following fields:
- optimized_instruction: string instruction that can be used to create the response given the request.
- output_format: Format of the output string. This should detail formatting constraints of the output. 
        Example output formats includes guidlines such as:
        e.g)    - 'Output should be a comma separated list'
                - 'Response should be as concise as possible'
                - 'Response should be json with keys a, b, c'
                - 'Response should not contains phrases like...'
                - 'Response should have the tone of ...'

- instruction_type: Enum that describes the type of instruction. Can be one of : {instruction_type_list}

The original instruction provided by the user is provided after the header `original_instruction`.
The list of criteria response must satisfy is provided after the header `response_criteria`

original_instruction: {instruction}
response_criteria: {response_criteria}
"""

INSTRUCTION_INFO_GENERATION_WITH_ICL = """
You are an expert in instruction analysis / generation. That is, given 
  - a list of JSON objects containing `request` and `response` keys
  - the original instruction provided by the user
  - List of criteria that response should satisfy

you should `infer` the OPTIMAL instruction to generate the response given the request. Instruction should be as detailed as possible.
The instruction info to generate has following fields.

- optimized_instruction: string instruction that can be used to create the response given the request.
- output_format: Format of the output string. This should detail formatting constraints of the output. 
        Example output formats includes guidlines such as:
        e.g)    - 'Output should be a comma separated list'
                - 'Response should be as concise as possible'
                - 'Response should be json with keys a, b, c'
                - 'Response should not contains phrases like...'
                - 'Response should have the tone of ...'

- instruction_type: Enum that describes the type of instruction. Can be one of : {instruction_type_list}

The original instruction provided by the user is provided after the header `original_instruction`.
The list of JSON objects containing `request` and `response` keys is provided after the header `example_data`.
The list of criteria response must satisfy is provided after the header `response_criteria`

example_data: {data}
original_instruction: {instruction}
response_criteria: {response_criteria}
"""


def populate_instruction_info(system_params: T2TSystemParams):
    instruction_type_list = f"{ ', '.join(str(v.name) for v in InstructionType) }"
    example_data = system_params.labelled_training_examples[:10]
    if example_data:
        system_msg = INSTRUCTION_INFO_GENERATION_WITH_ICL.format(data=example_data,
                                                                 instruction=system_params.instruction,
                                                                 instruction_type_list=instruction_type_list,
                                                                 response_criteria=system_params.evaluation_criteria)
    else:
        system_msg = INSTRUCTION_INFO_GENERATION_WITHOUT_ICL.format(instruction=system_params.instruction,
                                                                    instruction_type_list=instruction_type_list,
                                                                    response_criteria=system_params.evaluation_criteria)

    messages = [{"role": "system", "content": system_msg}]
    instruction_info = generate_base_model_using_chat_completion_messages(messages,
                                                                          InstructionInfo,
                                                                          model_id="gpt-4o-2024-08-06-text2text")
    system_params.instruction_info = instruction_info
