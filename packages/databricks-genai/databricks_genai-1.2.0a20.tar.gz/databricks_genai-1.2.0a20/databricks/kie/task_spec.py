"""Defines the task spec for KIE"""
import os
import re
import tempfile
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, model_validator

from databricks.kie.data_utils import IGNORED_CACHE_ROOT, get_valid_files
from databricks.model_training.api.exceptions import ValidationError
from databricks.model_training.api.utils import (check_if_table_exists, check_table_has_columns, format_table_name,
                                                 get_me, get_schema_from_table, get_spark, normalize_table_name,
                                                 table_schema_overlaps)
from databricks.model_training.api.validation import (validate_delta_table, validate_uc_path_write_permissions,
                                                      validate_uc_permissions)


def get_default_experiment_name_with_suffix(suffix: str) -> str:
    """Returns a default experiment name with a suffix.

    Args:
        suffix: Suffix to append to the default experiment name

    Returns: Experiment name in format /Users/{username}/{suffix} .
    """
    username = get_me()
    return f"/Users/{username}/{suffix}"


class KIETaskSpec(BaseModel):
    """Task spec for KIE experiments"""
    unlabeled_dataset: Optional[str]
    unlabeled_delta_table: Optional[str]
    unlabeled_delta_table_text_column: Optional[str]
    json_examples: List[Dict[str, Any]]
    experiment_name: str
    labeled_dataset: Optional[str]
    labeled_dataset_text_column: Optional[str]
    labeled_dataset_output_json_column: Optional[str]
    output_path: str
    output_table: str

    @staticmethod
    def _get_experiment_basename(unlabeled_dataset: Optional[str], unlabeled_delta_table: Optional[str]) -> str:
        assert unlabeled_dataset or unlabeled_delta_table
        if unlabeled_dataset:
            basename = os.path.basename(unlabeled_dataset.rstrip("/"))
        else:
            basename = unlabeled_delta_table.split(".")[-1]
        return basename.replace("_", "-").lower()

    @staticmethod
    def _get_default_output_path(unlabeled_dataset: str, experiment_name: str) -> str:
        # Default to a cache folder in the dataset
        # For delta tables, we require that output_path is already provided, since it can't be inferred
        root_name = format_table_name(os.path.basename(experiment_name))
        return os.path.join(unlabeled_dataset, f"{IGNORED_CACHE_ROOT}{root_name}")

    @staticmethod
    def _get_default_output_table(output_path: str, unlabeled_dataset: Optional[str],
                                  unlabeled_delta_table: Optional[str]) -> str:
        # If unlabeled_delta_table is provided, we will create a new table in the same schema
        if unlabeled_delta_table:
            output_schema = ".".join(unlabeled_delta_table.split(".")[:2])
        else:
            output_schema = ".".join(output_path.split("/")[2:4])
        # Get the basename for the dataset
        dataset_name = KIETaskSpec._get_experiment_basename(unlabeled_dataset, unlabeled_delta_table)
        # If we are using a unlabeled_delta_table, we add a prefix to avoid conflicts with existing delta table
        if unlabeled_delta_table:
            dataset_name = f"kie_output_{dataset_name}"
        # Format the table name correctly
        dataset_name = format_table_name(dataset_name)
        return f"{output_schema}.{dataset_name}"

    @staticmethod
    def _get_default_experiment_name(unlabeled_dataset: Optional[str], unlabeled_delta_table: Optional[str]) -> str:
        # Choose a default experiment name
        unlabeled_dataset_name = KIETaskSpec._get_experiment_basename(unlabeled_dataset, unlabeled_delta_table)
        return get_default_experiment_name_with_suffix(f"kie-{unlabeled_dataset_name}")

    @classmethod
    def create(
        cls,
        unlabeled_dataset: Optional[str],
        unlabeled_delta_table: Optional[str],
        unlabeled_delta_table_text_column: Optional[str],
        json_examples: List[Dict[str, Any]],
        experiment_name: Optional[str],
        labeled_dataset: Optional[str],
        labeled_dataset_text_column: Optional[str],
        labeled_dataset_output_json_column: Optional[str],
        output_path: Optional[str],
        output_table: Optional[str],
    ) -> 'KIETaskSpec':

        if not unlabeled_dataset and not unlabeled_delta_table:
            raise ValueError(
                "Please provide an unlabeled_dataset or an unlabeled_delta_table (with the corresponding text column)")

        if unlabeled_dataset and unlabeled_delta_table:
            raise ValueError(
                "Please provide only one of unlabeled_dataset or unlabeled_delta_table (with the related text column)")

        if unlabeled_dataset:
            unlabeled_dataset = unlabeled_dataset.rstrip("/")

        if experiment_name is None:
            # Choose a default experiment name based on the dataset name
            experiment_name = cls._get_default_experiment_name(unlabeled_dataset, unlabeled_delta_table)

        if unlabeled_delta_table and not output_path:
            raise ValueError("Please provide an output_path if you are using a delta table for the unlabeled dataset")

        if output_path is None:
            assert unlabeled_dataset, "unlabeled_dataset is required if output_path is not provided"
            output_path = cls._get_default_output_path(unlabeled_dataset, experiment_name=experiment_name)

        if output_table is None:
            output_table = cls._get_default_output_table(output_path, unlabeled_dataset, unlabeled_delta_table)

        return cls(
            unlabeled_dataset=unlabeled_dataset,
            unlabeled_delta_table=unlabeled_delta_table,
            unlabeled_delta_table_text_column=unlabeled_delta_table_text_column,
            json_examples=json_examples,
            experiment_name=experiment_name,
            labeled_dataset=labeled_dataset,
            labeled_dataset_text_column=labeled_dataset_text_column,
            labeled_dataset_output_json_column=labeled_dataset_output_json_column,
            output_path=output_path,
            output_table=normalize_table_name(output_table),
        )

    @model_validator(mode='after')
    def validate_spec(self: 'KIETaskSpec') -> 'KIETaskSpec':
        try:
            return validate_task_spec(self)
        except ValidationError as e:
            # Re-raise validation errors for pydantic
            raise ValueError(str(e)) from e


def validate_can_read_from_unlabeled_dataset(unlabeled_dataset: str):
    try:
        os.listdir(unlabeled_dataset)
    except OSError as e:
        raise ValueError(f"Could not read from unlabeled dataset at {unlabeled_dataset}. " +
                         "Please make sure the path is correct and you have read permissions.") from e


def validate_schema_starting_point(task_spec: KIETaskSpec):
    if not task_spec.json_examples and not task_spec.labeled_dataset:
        raise ValueError("Please provide example JSON outputs so we can know what to extract")


def validate_output_write_permissions(output_path: str):

    if os.path.isdir(output_path):
        # Check if the user has write permissions to the output path
        validate_uc_path_write_permissions(output_path)
        return

    # Check if the user has write permissions to the parent directory of the output path
    try:
        # Test creating a temporary file in the parent directory of the output path
        # This mocks the ability to create the directory and write to it
        testfile = tempfile.TemporaryFile(dir=os.path.dirname(output_path))
        testfile.close()
    except OSError as e:
        raise ValueError(f"Could not create output folder at {output_path}. " +
                         "Please make sure you have write permissions to the parent directory, " +
                         "or specify an `output_path` where you do") from e


def validate_valid_output_path(output_path: str, unlabeled_dataset: Optional[str]):
    if unlabeled_dataset and output_path.rstrip("/") == unlabeled_dataset.rstrip("/"):
        raise ValueError(
            "Output path cannot be the same as the unlabeled dataset. Please provide a different output path")

    if "." in output_path:
        raise ValueError("Output path cannot contain a '.' character. Please provide a different output path")


def validate_output_table_name(output_table: str):
    names = output_table.split(".")
    if len(names) != 3:
        raise ValueError("Output table name must be in the format `catalog.schema.table`")
    for name in names:
        if re.match(r'^[a-zA-Z0-9_`-]+$', name) is None:
            raise ValueError("Output table name must only contain alphanumeric characters, underscores, and hyphens.")


def validate_delta_table_is_valid(dataset: str, columns_and_names: List[Tuple[str, str]]):
    spark = get_spark()
    df = spark.read.table(dataset)
    schema = dict(df.dtypes)
    for column_name, user_provided_name in columns_and_names:
        if user_provided_name not in schema:
            raise ValueError(f"The provided {column_name} {user_provided_name} is not in the table. " +
                             "Please check your configuration.")

    # If we have the following columns, we will have issues in other steps since we never isolate columns
    # response: (grounding.py:L29) The table will have two `response` columns which can't be saved
    # extracted_response: (inference_utils.py:L97) The table will have two `extracted_response` columns
    # raw_response: (inference_utils.py:L96) The table will have two `raw_response` columns
    # Note: Other columns like "rand", "row_id", etc that will be overwritten and can lead to edge case issues
    check_protected_columns(dataset, ["response", "extracted_response", "raw_response"])


def validate_unlabeled_delta_table_is_valid(unlabeled_dataset: str, unlabeled_delta_table_text_column: str):
    columns_and_names = [
        ("unlabeled_delta_table_text_column", unlabeled_delta_table_text_column),
    ]
    validate_delta_table_is_valid(unlabeled_dataset, columns_and_names)


def validate_labeled_dataset_is_valid(labeled_dataset: str, labeled_dataset_text_column: str,
                                      labeled_dataset_output_json_column: str):
    columns_and_names = [
        ("labeled_dataset_text_column", labeled_dataset_text_column),
        ("labeled_dataset_output_json_column", labeled_dataset_output_json_column),
    ]
    validate_delta_table_is_valid(labeled_dataset, columns_and_names)


def validate_row_count_table(table_name: str, required_count: int = 10, recommended_count: int = 1000) -> None:
    spark = get_spark()
    df = spark.read.table(table_name)
    row_count = df.count()
    validate_row_count(row_count, required_count, recommended_count)


def validate_row_count_dataset(dataset: str, required_count: int = 10, recommended_count: int = 1000) -> None:
    row_count = len(get_valid_files(dataset))
    validate_row_count(row_count, required_count, recommended_count)


def validate_row_count(
    row_count: int,
    required_count: int = 10,
    recommended_count: int = 1000,
) -> None:
    if row_count < required_count:
        raise ValueError(f'Insufficient data. We require at least {required_count} unlabeled examples ' +
                         f'(recommend at least {recommended_count}). Found only {row_count} examples.')
    if row_count < recommended_count:
        print(f'Warning: Found {row_count} unlabeled examples, ' +
              f'we recommend at least {recommended_count} for best results.')


def check_protected_columns(table_name: str, protected_columns: List[str]):
    if overlapping_columns := table_schema_overlaps(table_name, protected_columns):
        raise ValueError(f"Table {table_name} already has the columns named {overlapping_columns}. "
                         "Please use different column names as this is a conflict.")


def validate_task_spec(task_spec: KIETaskSpec) -> KIETaskSpec:
    # validate that one of the following is provided

    if task_spec.unlabeled_dataset:
        # Validate that you can read from the unlabeled dataset
        validate_can_read_from_unlabeled_dataset(task_spec.unlabeled_dataset)

        # Validate that we have enough unlabeled data to do anything
        validate_row_count_dataset(task_spec.unlabeled_dataset)

    if task_spec.unlabeled_delta_table:
        # Validate that you can access the unlabeled_delta_table
        validate_delta_table(task_spec.unlabeled_delta_table, "unlabeled_delta_table")

        # Validate the unlabeled delta table is valid
        validate_unlabeled_delta_table_is_valid(task_spec.unlabeled_delta_table,
                                                task_spec.unlabeled_delta_table_text_column)

        # Validate that we have enough unlabeled data to do anything
        validate_row_count_table(task_spec.unlabeled_delta_table)

    # Validate that we have some schema starting point
    validate_schema_starting_point(task_spec)

    # Validate that the output path is valid
    validate_valid_output_path(task_spec.output_path, task_spec.unlabeled_dataset)

    # Validate permission to write create an output cache folder
    validate_output_write_permissions(task_spec.output_path)
    print(f"✔ Validated write permissions to output_path: {task_spec.output_path}")

    # Validate output table has valid characters
    validate_output_table_name(task_spec.output_table)

    # Validate we can write to the output schema
    output_schema = get_schema_from_table(task_spec.output_table)
    validate_uc_permissions(output_schema, 'schema', ['ALL_PRIVILEGES', 'USE_SCHEMA'], input_name='output_schema')

    # Ensure the output table doesn't already exist
    if check_if_table_exists(task_spec.output_table):
        # If output_table already exists, the user may be repeating KIE
        # Verify that it has a "request" column
        if not check_table_has_columns(task_spec.output_table, ("request",)):
            raise ValueError(f"Output table {task_spec.output_table} already exists, " +
                             "but does not seem to be from a KIE experiment. Please choose a different path.")

    print(f"✔ Validated write permissions to output_table: {task_spec.output_table}")

    # Validate the labeled dataset and ensure all columns specified exist
    if task_spec.labeled_dataset:
        # Validate that you can access the labeled_dataset
        validate_delta_table(task_spec.labeled_dataset, "labeled_dataset")

        # Validate the labeled dataset is valid
        validate_labeled_dataset_is_valid(task_spec.labeled_dataset, task_spec.labeled_dataset_text_column,
                                          task_spec.labeled_dataset_output_json_column)
        print(f"✔ Validated permissions and contents of labeled_dataset: {task_spec.labeled_dataset}")

    print("✔ Validation checks passed!")
    return task_spec
