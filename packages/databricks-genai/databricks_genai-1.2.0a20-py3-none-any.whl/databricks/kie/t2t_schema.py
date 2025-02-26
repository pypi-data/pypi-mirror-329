"""Module representing the schema / dataclass for Text2Text module."""
import itertools
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

import mlflow
from pydantic import BaseModel, Field

from databricks.kie.data_utils import partition_data, read_from_jsonl, read_from_table_with_columns

MAX_EXAMPLES_PER_DATA_SOURCE = 200


@dataclass
class JsonlFileDataConfig:
    """Jsonl file data configuration"""
    file_path: str
    input_key: str
    output_key: str


@dataclass
class UCTableDataConfig:
    """Unity catalog table data configuration"""
    table_path: str
    input_column_name: str
    output_column_name: str


@dataclass
class PreferenceData:
    """Preference data for a T2T model."""
    input: str
    rejected_response: str
    preferred_response: str


@dataclass
class Text2TextTaskSpec:
    """Task spec for Text2Text experiments"""
    instruction: str
    experiment_name: Optional[str] = None
    json_examples: Optional[List[Dict[str, str]]] = field(default_factory=list)
    uc_table: Optional[UCTableDataConfig] = None
    jsonl_file: Optional[JsonlFileDataConfig] = None
    evaluation_criteria: Optional[List[str]] = None
    run_id: Optional[str] = None

    def __post_init__(self):
        if not self.json_examples and not self.uc_table and not self.jsonl_file:
            raise ValueError("Missing data config for Text2Text -- one of `json_examples`, `uc_table`, `jsonl_file`"
                             " should be provided")

        return self

    def get_user_labelled_data(self) -> List[PreferenceData]:
        """Get the user labelled data from previous session.

        Returns:
            List[PreferenceData]: The user labelled preferencedata.
        """
        if not self.run_id:
            return []

        traces = mlflow.search_traces(run_id=self.run_id)
        preference_data = []
        for trace in traces:
            dict_info = trace.to_pandas_dataframe_row()
            request, response = dict_info.get('request'), dict_info.get('response')
            if not request or not response:
                continue

            # TODO(jun.choi): Use the correct API once SME labelling API is ready.
            # For now, we assume that the target is always present in the tags.
            # TODO(jun.choi): Support sparse data such as user thumbs up / down.
            # Using tags based approach.
            tags = dict_info['tags']
            if 'target' not in tags:
                continue

            preference_data.append(
                PreferenceData(input=request, rejected_response=response, preferred_response=tags['target']))
        return preference_data

    def to_system_param(self) -> 'T2TSystemParams':
        """Converts the task spec to system params for a Text2Text model"""
        # TODO(jun.choi): Support unlabelled examples.
        labelled_examples = []
        if self.uc_table:
            columns = (self.uc_table.input_column_name, self.uc_table.output_column_name)
            table_data = read_from_table_with_columns(self.uc_table.table_path,
                                                      columns,
                                                      MAX_EXAMPLES_PER_DATA_SOURCE,
                                                      filter_null_value=True)
            for datum in table_data:
                labelled_examples.append(
                    (datum[self.uc_table.input_column_name], datum[self.uc_table.output_column_name]))

        if self.json_examples:
            for datum in self.json_examples:
                if not set(datum.keys()) >= {'request', 'response'}:
                    raise ValueError("Invalid json example format. Should have keys 'request' and 'response'")

                labelled_examples.append((datum['request'], datum['response']))

        if self.jsonl_file:
            data = read_from_jsonl(self.jsonl_file.file_path, MAX_EXAMPLES_PER_DATA_SOURCE)
            for datum in data:
                labelled_examples.append((datum[self.jsonl_file.input_key], datum[self.jsonl_file.output_key]))

        train_data, test_data = partition_data(labelled_examples, min_test_data_size=5, test_set_ratio=0.5)
        preference_data = self.get_user_labelled_data()

        return T2TSystemParams(instruction=self.instruction,
                               labelled_training_examples=train_data,
                               labelled_test_examples=test_data,
                               evaluation_criteria=self.evaluation_criteria,
                               preference_data=preference_data)


class InstructionType(str, Enum):
    classification = "classification"
    grounded_generation = "grounded_generation"
    subspan_extraction = "subspan_extraction"
    summarization = "summarization"
    others = "others"


# TODO(jun.choi): Add `optimized_instruction` in InstructionSchema via DSPY
class InstructionInfo(BaseModel):
    optimized_instruction: str = Field(
        description="""Instruction optimized for the model. Includes detailed guidelines including
        1. Instruction / task description.
        2. Nature of the input to be provided.
        3. Expected response format.
        4. Constraints on the response or criteria tat the response should satisfy.
        """)
    instruction_type: InstructionType = Field(description=("Task type of of the instruction. Can be one of :"
                                                           f"{', '.join(str(v.name) for v in InstructionType)}"))
    output_format: str = Field(
        description=("The format of the output response. For example "
                     "'Output should be a comma separated list' / 'Response should be as concise as possible' "))


@dataclass
class T2TSystemParams:
    """System parameters for a T2T model."""
    instruction: str
    instruction_info: Optional[InstructionInfo] = None
    unlabelled_examples: Optional[List[str]] = None
    labelled_training_examples: Optional[List[Tuple[str, str]]] = None
    labelled_test_examples: Optional[List[Tuple[str, str]]] = None
    evaluation_criteria: Optional[List[str]] = None
    preference_data: Optional[List[PreferenceData]] = None

    def __post_init__(self):
        if not self.unlabelled_examples and not self.labelled_training_examples and not self.labelled_test_examples:
            raise ValueError("One of labelled or unlabelled examples should be provided")
        return self

    def get_sxs_data(self, other: 'T2TSystemParams') -> List[Dict[str, str]]:
        """Get side by side data that can be used to comapre this and another T2TSystemParams."""
        common_unlabelled = set(self.unlabelled_examples or []).intersection(set(other.unlabelled_examples or []))
        common_labelled = set(self.labelled_test_examples or []).intersection(set(other.labelled_test_examples or []))
        data = []
        for datum in sorted(itertools.chain(common_unlabelled, common_labelled)):
            if isinstance(datum, str):
                data.append({'request': datum})
            else:
                data.append({'request': datum[0], 'response': datum[1]})
        return data

    def get_diff(self, other: 'T2TSystemParams') -> 'T2TSystemParamsDiff':
        """Get the differences between this and another T2TSystemParams.

        Returns: T2TSystemParamsDiff object containing fields (self - other).
        """
        diff = {}
        if self.instruction != other.instruction:
            diff['instruction'] = self.instruction
            diff['previous_instruction'] = other.instruction

        evaluation_criteria_diff = list(set(self.evaluation_criteria or []) - set(other.evaluation_criteria or []))
        if evaluation_criteria_diff:
            diff['evaluation_criteria'] = evaluation_criteria_diff

        added_labeled_example_diff = (
            list(set(self.labelled_training_examples or []) - set(other.labelled_training_examples or [])))
        removed_labeled_example_diff = (
            list(set(other.labelled_training_examples or []) - set(self.labelled_training_examples or [])))
        added_unlabeled_example_diff = (
            list(set(self.unlabelled_examples or []) - set(other.unlabelled_examples or [])))
        removed_unlabeled_example_diff = (
            list(set(other.unlabelled_examples or []) - set(self.unlabelled_examples or [])))
        diff['added_labelled_examples'] = added_labeled_example_diff
        diff['removed_labelled_examples'] = removed_labeled_example_diff
        diff['added_unlabelled_examples'] = added_unlabeled_example_diff
        diff['removed_unlabelled_examples'] = removed_unlabeled_example_diff
        return T2TSystemParamsDiff(**diff)


@dataclass
class T2TSystemParamsDiff:
    """System parameters diff between 2 versions of T2T model."""
    previous_instruction: Optional[str] = None
    instruction: Optional[str] = None
    evaluation_criteria: Optional[List[str]] = None
    added_labelled_examples: Optional[List[Tuple[str, str]]] = None
    removed_labelled_examples: Optional[List[Tuple[str, str]]] = None
    added_unlabelled_examples: Optional[List[str]] = None
    removed_unlabelled_examples: Optional[List[str]] = None


@dataclass
class SideBySideResult:
    """Side by side results for a T2T model"""
    request: str
    previous_response: str
    current_response: str


@dataclass
class T2TSystemResult:
    """Model evaluation result for a T2T model"""
    eval_result: mlflow.models.EvaluationResult
    examples: List[Tuple[str, str]]
    sxs_result: Optional[List[SideBySideResult]]
    current_task_spec: Text2TextTaskSpec
    experiment_id: str
    model_candidates: List[str]
    default_model: str
    instruction_info: InstructionInfo
