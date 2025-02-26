"""Functions for creating evaluation criteria."""

import json
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field

from databricks.kie.inference_utils import generate_base_model_using_chat_completion_messages
from databricks.kie.t2t_schema import PreferenceData

_EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT = (
    "You are an expert at user instruction analysis. "
    "Given an instruction for any task provided by the user, return a JSON list of criteria."
    "The criteria will be used to score an LLM on how well it followed the instructions given a specific input."
    "Provide detailed granular evaluation criteria on fomatting, style, and correctness."
    "Instruction to analyze is provided in in user message following 'Instruction' header."
    "Provide detailed granular evaluation criteria on fomatting, style, and correctness.")

_EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT_WITH_EXAMPLES = (
    "You are an expert at user instruction analysis. "
    "Given an instruction for any task provided by the user and a JSON containing ground truth request"
    " and response pairs, return a JSON list of criteria."
    "The criteria will be used to score an LLM on how well it followed the instructions given a specific input."
    "Instruction to analyze is provided in in user message following 'Instruction' header, "
    "and examples are provided in user message following 'Ground Truth Examples' header."
    "Provide detailed granular evaluation criteria on fomatting, style, and correctness.")

_EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT_FROM_PREFERENCE = (
    "You are an expert at error analysis. "
    "Given an instruction for a task provided by the user and a JSON containing the input, incorrect "
    "output, and correct output, return a JSON list of differences between the incorrect and"
    "correct output. "
    "The criteria will be used to score an LLM on how well it followed the instructions given a specific input. "
    "Instruction to analyze is provided in in user message following 'Instruction' header, "
    "and examples are provided in user message following 'Examples' header. "
    "Provide specific evaluation criteria about the differences between the incorrect and correct output. "
    "Only provide the differences, not the similarities. If the criteria is the same, do not repeat it. "
    "Make sure the differences are between the incorrect and correct output, not just a difference between the "
    "input and incorrect output. "
    "Generalize the differences as criteria to apply to all examples")

_DEDUPE_EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT = (
    "You are an expert at deduplicating lists of evaluation criteria. "
    "Given an instruction for a task provided by the user and a list of the old criteria and a list of the "
    "new criteria, return a JSON list of criteria combining the two. "
    "The criteria will be used to score an LLM on how well it followed the instructions given a specific input. "
    "Instruction to analyze is provided in in user message following 'Instruction' header, "
    "the old criteria are provided in user message following 'Old criteria' header, "
    "and the new criteria are provided in user message following 'New criteria' header. "
    "Do not repeat criteria that are the same. If there are contradictory criteria between the old criteria "
    "and the new criteria, the new criteria takes priority.")


class EvaluationCriteria(BaseModel):
    criteria: List[str] = Field(description="List of evaluation criteria that the response must satisfy.")


def generate_evaluation_criteria(instruction: str, examples: Optional[List[Tuple[str, str]]] = None) -> List[str]:
    """Generates list of evaluation criteria based on the given instruction and examples.

    Args:
        instruction (str): The instruction to generate evaluation criteria for.
        examples (list, optional): A list of tuple (input, output) containing ground truth request and response pairs.
            Defaults to None.

    Returns:
        list: A list of generated evaluation criteria.
    """
    if examples:
        examples = [{"request": example[0], "response": example[1]} for example in examples]

    messages = [{
        "role":
            "system",
        "content":
            _EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT_WITH_EXAMPLES if examples else _EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT
    }, {
        "role":
            "user",
        "content": (f"Instruction: {instruction}\n\n Ground Truth Examples: {json.dumps(examples)}"
                    if examples else f"Instruction: {instruction}")
    }]

    return generate_base_model_using_chat_completion_messages(messages,
                                                              EvaluationCriteria,
                                                              model_id="gpt-4o-2024-08-06-text2text").criteria


def generate_evaluation_criteria_from_preference(instruction: str, preference_data: List[PreferenceData]) -> List[str]:
    """Generates list of evaluation criteria based on the given instruction and preference data.

    Args:
        instruction (str): The instruction to generate evaluation criteria for.
        preference_data (list): A list of preference data.

    Returns:
        list: A list of generated evaluation criteria.
    """
    examples = [{
        "input": example.input,
        "incorrect output": example.rejected_response,
        "correct output": example.preferred_response,
    } for example in preference_data]

    messages = [{
        "role": "system",
        "content": _EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT_FROM_PREFERENCE
    }, {
        "role": "user",
        "content": f"Instruction: {instruction}\n\nExamples: {json.dumps(examples)}"
    }]

    return generate_base_model_using_chat_completion_messages(messages,
                                                              EvaluationCriteria,
                                                              model_id="gpt-4o-2024-08-06-text2text").criteria


def dedupe_evaluation_criteria(instruction: str, old_criteria: List[str], new_criteria: List[str]) -> List[str]:
    """Generates list of evaluation criteria based on the given instruction and criteria.

    The generated list of evaluation criteria combines the old criteria and new criteria, deduplicating similar
    criteria and giving preference to the new criteria if conflicts exist.

    Args:
        instruction (str): The instruction to generate evaluation criteria for.
        old_criteria (list): A list of old evaluation criteria.
        new_criteria (list): A list of new evaluation criteria.

    Returns:
        list: A list of deduped evaluation criteria.
    """

    messages = [{
        "role": "system",
        "content": _DEDUPE_EVAL_CRITERIA_GENERATOR_SYSTEM_PROMPT
    }, {
        "role":
            "user",
        "content": (f"Instruction: {instruction}\n\nOld criteria: {json.dumps(old_criteria)}\n\n"
                    f"New criteria: {json.dumps(new_criteria)}")
    }]

    return generate_base_model_using_chat_completion_messages(messages,
                                                              EvaluationCriteria,
                                                              model_id="gpt-4o-2024-08-06-text2text").criteria


def add_evaluation_criteria_from_preference_data(
    instruction: str,
    evaluation_criteria: List[str],
    preference_data: List[PreferenceData],
) -> List[str]:
    """Generates list of evaluation criteria based on the given instruction, old criteria, and new examples.

    The examples are first used to generate a set of new criteria. The old critera and new criteria are then combined.

    Args:
        instruction (str): The instruction to generate evaluation criteria for.
        evaluation_criteria (list): A list of evaluation criteria.
        preference_data (list): A list of preference data.

    Returns:
        list: A list of updated evaluation criteria.
    """
    new_criteria = generate_evaluation_criteria_from_preference(instruction=instruction,
                                                                preference_data=preference_data)
    final_criteria = dedupe_evaluation_criteria(
        instruction=instruction,
        old_criteria=evaluation_criteria,
        new_criteria=new_criteria,
    )
    return final_criteria
