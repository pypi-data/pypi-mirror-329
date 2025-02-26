"""Module for creating Text2Text system."""
from typing import Dict, List, Optional

from databricks.kie.t2t_runner import Text2TextRunner
from databricks.kie.t2t_schema import JsonlFileDataConfig, Text2TextTaskSpec, UCTableDataConfig


class Text2TextFactory:
    """Factory class for creating Text2Text system."""

    @staticmethod
    def from_jsonl(instruction: str,
                   file_path: str,
                   input_key_name: str,
                   output_key_name: str,
                   experiment_name: Optional[str] = None,
                   evaluation_criteria: Optional[List[str]] = None):
        """Creates a Text2Text system from a jsonl file in UC Volume."""
        task_spec = Text2TextTaskSpec(instruction=instruction,
                                      jsonl_file=JsonlFileDataConfig(file_path=file_path,
                                                                     input_key=input_key_name,
                                                                     output_key=output_key_name),
                                      experiment_name=experiment_name,
                                      evaluation_criteria=evaluation_criteria)

        return Text2TextRunner(task_spec=task_spec)

    @staticmethod
    def from_uc_table(instruction: str,
                      table_path: str,
                      input_column_name: str,
                      output_column_name: str,
                      experiment_name: Optional[str] = None,
                      evaluation_criteria: Optional[List[str]] = None):
        """Creates a Text2Text system from Unity Catalog table."""
        task_spec = Text2TextTaskSpec(instruction=instruction,
                                      uc_table=UCTableDataConfig(table_path=table_path,
                                                                 input_column_name=input_column_name,
                                                                 output_column_name=output_column_name),
                                      experiment_name=experiment_name,
                                      evaluation_criteria=evaluation_criteria)
        return Text2TextRunner(task_spec=task_spec)

    @staticmethod
    def from_examples(instruction: str,
                      examples: List[Dict[str, str]],
                      experiment_name: Optional[str] = None,
                      evaluation_criteria: Optional[List[str]] = None):
        """Creates a Text2Text system from a list of examples."""
        task_spec = Text2TextTaskSpec(instruction=instruction,
                                      json_examples=examples,
                                      experiment_name=experiment_name,
                                      evaluation_criteria=evaluation_criteria)
        return Text2TextRunner(task_spec=task_spec)
