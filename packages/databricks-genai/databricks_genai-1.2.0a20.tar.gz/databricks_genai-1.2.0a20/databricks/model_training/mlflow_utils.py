"""mlflow utility functions for handling runs and metadata"""
import json
from enum import Enum
from typing import Dict, NamedTuple, Optional, Tuple, Union

from databricks.sdk import WorkspaceClient  # pylint: disable=ungrouped-imports
from mlflow import MlflowClient
from mlflow.data.delta_dataset_source import DeltaDatasetSource
from mlflow.data.meta_dataset import MetaDataset
from mlflow.data.uc_volume_dataset_source import UCVolumeDatasetSource
from mlflow.entities import DatasetInput, InputTag, SourceType
from mlflow.utils._spark_utils import _get_active_spark_session
from mlflow.utils.mlflow_tags import (MLFLOW_DATABRICKS_NOTEBOOK_ID, MLFLOW_DATABRICKS_NOTEBOOK_PATH,
                                      MLFLOW_DATASET_CONTEXT, MLFLOW_SOURCE_NAME, MLFLOW_SOURCE_TYPE)

from databricks.model_training.api.utils import get_current_notebook_details

_ACTIVE_CATALOG_QUERY = "SELECT current_catalog() AS catalog"
_ACTIVE_SCHEMA_QUERY = "SELECT current_database() AS schema"


def get_mlflow_client() -> MlflowClient:
    return MlflowClient(tracking_uri="databricks", registry_uri="databricks-uc")


class DatasetType(Enum):
    DELTA_TABLE = "delta_table"
    UC_VOLUME = "uc_volume"


class DatasetSource(NamedTuple):
    dataset_type: DatasetType
    dataset_path: str


class DeltaTableDetails(NamedTuple):
    catalog: Optional[str]
    name: Optional[str]
    full_name: Optional[str]
    version: Optional[int]


def get_delta_table_details(path: str) -> DeltaTableDetails:
    w = WorkspaceClient()
    details = w.tables.get(path, include_delta_metadata=True)
    version = None
    if details.delta_runtime_properties_kvpairs:
        if details.delta_runtime_properties_kvpairs.delta_runtime_properties:
            attributes = details.delta_runtime_properties_kvpairs.delta_runtime_properties.get("commitAttributes")
            if attributes:
                version = json.loads(attributes)["version"]

    return DeltaTableDetails(catalog=details.catalog_name,
                             name=details.name,
                             full_name=details.full_name,
                             version=version)


def log_source_as_input(run_id: str,
                        source: Union[DeltaDatasetSource, UCVolumeDatasetSource],
                        name: str = "Dataset",
                        split: Optional[str] = None):
    client = get_mlflow_client()

    meta = MetaDataset(source, name=name)

    # Contstruct the entities
    tags = [InputTag(key=MLFLOW_DATASET_CONTEXT, value=split)] if split else []
    inputs = [DatasetInput(dataset=meta._to_mlflow_entity(), tags=tags)]  # pylint: disable=protected-access

    return client.log_inputs(run_id=run_id, datasets=inputs)


def log_delta_table_source(run_id: str, path: str, name: str = "Dataset", split: Optional[str] = None):
    """
    Log a delta table as a dataset input to an MLflow run.
    
    Args:
        run_id (str): The MLflow run ID.
        path (str): The path to the delta table.
        name (str, optional): The name of the dataset. Defaults to "Dataset".
        split (str, optional): The data split (e.g., "train", "test"). Defaults to None.
    
    Returns:
        None
    """

    # Get the source delta table
    table_details = get_delta_table_details(path)
    source = DeltaDatasetSource(delta_table_name=path, delta_table_version=table_details.version)
    return log_source_as_input(run_id, source, name=name, split=split)


def log_uc_volume_source(run_id: str, path: str, name: str = "Dataset", split: Optional[str] = None):
    """
    Logs a Unity Catalog (UC) volume source as an input to an MLflow run.
    
    Args:
        run_id (str): The ID of the MLflow run.
        path (str): The path to the UC volume source.
        name (str, optional): The name of the dataset. Defaults to "Dataset".
        split (str, optional): The data split (e.g., "train", "test"). Defaults to None.
    
    Returns:
        None
    """

    # Get the source delta table
    source = UCVolumeDatasetSource(path)
    return log_source_as_input(run_id, source, name=name, split=split)


def update_run_tags(run_id: str, tags: Dict[str, str]):
    client = get_mlflow_client()
    for k, v in tags.items():
        client.set_tag(run_id, k, v)


def change_run_name(run_id: str, new_name: str) -> None:
    client = get_mlflow_client()
    return client.update_run(run_id=run_id, name=new_name)


def add_notebook_source(run_id: str):
    details = get_current_notebook_details()
    if not details:
        return
    tags = {
        MLFLOW_SOURCE_NAME: details.notebook_path,
        MLFLOW_SOURCE_TYPE: SourceType.to_string(SourceType.NOTEBOOK),
        MLFLOW_DATABRICKS_NOTEBOOK_PATH: details.notebook_path,
        MLFLOW_DATABRICKS_NOTEBOOK_ID: details.notebook_id,
    }
    update_run_tags(run_id, tags)


def get_default_model_registry_path_info() -> Tuple[str, str]:
    """Returns the default model registry catalog and schema."""
    spark = _get_active_spark_session()
    catalog = spark.sql(_ACTIVE_CATALOG_QUERY).collect()[0]['catalog']
    schema = spark.sql(_ACTIVE_SCHEMA_QUERY).collect()[0]['schema']
    return catalog, schema
