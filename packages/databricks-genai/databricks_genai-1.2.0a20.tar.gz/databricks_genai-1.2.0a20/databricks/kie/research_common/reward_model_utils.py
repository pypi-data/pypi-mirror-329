"""Module containing the utility functions related to reward model."""
from typing import Optional

from pydantic import BaseModel, Field

from databricks.kie.t2t_utils import (create_chat_completions_messages_from_instruction,
                                      create_structured_outputs_using_cot)

PROMPT_COMPLEXITY_RATING_DESCRIPTION = """Rate the complexity of the prompt:
(1-very easy), (2-easy), (3-normal), (4-complex), (5-very complex).
For example, 
    - (1-very easy) prompt might be a simple yes or no question, 
    - (3-normal) prompt might require a bit of thought or some specific memorable knowledge 
    - (5-very complex) prompt might require complex reasoning and/or breaking down the question 
        into multiple subquestions and/or require expertise of PhD level human.
"""

PROMPT_COMPLEXITY_RATING_SYSTEM_PROMPT = """
You are an advanced annotator AI able to simulate the expert judgement of a top level human annotator. 
Your task is to analyze a prompt given by the user and label its complexity.

## Input
You will receive a user prompt in the under the following header format: ## prompt_to_analyze

## Task
You goal is to label the complexity & difficulty of the prompt.

## Output
You should output the complexity rating of the prompt as rating integer between 1 and 5.
1 being the easiest and 5 being the hardest.
"""

REWARD_RATING_DESCRIPTION = """Rate the quality of the response:
(1-very bad), (2-bad), (3-normal), (4-good), (5-very good).
For example, 
    - (1-very bad) response might be a response that is not helpful, incorrect, or not relevant to the prompt.
    - (3-normal) response might be a response that is helpful, correct, and relevant to the prompt.
    - (5-very good) response might be a response that is helpful, correct, and relevant to the prompt.
"""

REWARD_RATING_SYSTEM_PROMPT = """
You are an advanced annotator AI able to simulate the expert judgement of a top level human annotator. 
Your task is to analyze a response given by the user and label its quality.

## Input
You will receive a user prompt and a response.
Prompt will be provided under the following header format: ## prompt_to_analyze
Response will be provided under the following header format: ## response_to_analyze

## Task
You goal is to label the quality of the response.

## Output
You should output the quality rating of the response as rating integer between 1 and 5.
1 being the worst and 5 being the best.
"""

COMPLEXITY_RATING_USER_PROMPT_TEMPLATE = """
## prompt_to_analyze: '{prompt}'
"""

REWARD_RATING_USER_PROMPT_TEMPLATE = """
## prompt_to_analyze: '{prompt}'
## response_to_analyze: '{response}'
"""

DEFAULT_CONTEXT_REWARD_MODEL_ID = "gpt-4o-2024-08-06-text2text"


class PromptComplexityRating(BaseModel):
    rating: int = Field(description=PROMPT_COMPLEXITY_RATING_DESCRIPTION)


class RewardRating(BaseModel):
    rating: int = Field(description=REWARD_RATING_DESCRIPTION)


def generate_prompt_complexity_rating(prompt: str, model_id: Optional[str] = DEFAULT_CONTEXT_REWARD_MODEL_ID) -> int:
    """
    Generate a rating based reward value for a given prompt and response.

    Args:
        prompt (str): The input prompt to evaluate along with the response.
        model_id (str): The model id to use for generating the reward value.

    Returns:
        int: The reward value between 1 and 10.
    """
    messages = create_chat_completions_messages_from_instruction(
        instruction=PROMPT_COMPLEXITY_RATING_SYSTEM_PROMPT,
        inp=COMPLEXITY_RATING_USER_PROMPT_TEMPLATE.format(prompt=prompt))
    return create_structured_outputs_using_cot(PromptComplexityRating, messages, model_id).rating


def generate_reward_rating(prompt: str,
                           response: str,
                           model_id: Optional[str] = DEFAULT_CONTEXT_REWARD_MODEL_ID) -> int:
    """
    Generate a rating based reward value for a given prompt and response.

    Args:
        prompt (str): The input prompt to evaluate along with the response.
        response (str): The response to generate the reward value for.
        model_id (str): The model id to use for generating the reward value.

    Returns:
        int: The reward value between 1 and 10.
    """
    messages = create_chat_completions_messages_from_instruction(instruction=REWARD_RATING_SYSTEM_PROMPT,
                                                                 inp=REWARD_RATING_USER_PROMPT_TEMPLATE.format(
                                                                     prompt=prompt, response=response))
    return create_structured_outputs_using_cot(RewardRating, messages, model_id).rating
