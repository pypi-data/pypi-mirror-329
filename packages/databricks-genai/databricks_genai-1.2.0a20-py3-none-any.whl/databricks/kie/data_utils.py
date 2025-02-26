"""Simple utils for working with KIE datasets"""
import json
import os
import random
import shutil
import tempfile
from copy import deepcopy
from functools import wraps
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type

import pandas as pd
from pydantic import BaseModel, ValidationError
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import monotonically_increasing_id, rand, udf
from pyspark.sql.types import StringType, StructField, StructType
from pyspark.sql.window import Window

from databricks.kie.kie_evaluator import parse_json_markdown
from databricks.model_serving.types.pt_endpoint import BaseEndpoint
from databricks.model_training.api.utils import check_if_table_exists, check_table_has_columns, get_spark

VALID_EXTENSIONS = {
    '.c', '.cpp', '.cs', '.css', '.go', '.html', '.java', '.js', '.json', '.md', '.php', '.py', '.rb', '.sh', '.tex',
    '.ts', '.txt', '.log', ''
}

MIN_LABELED_TRAIN_SAMPLES = 100
MIN_DOCS_TO_TRAIN = 50
MAX_DOCS_TO_TRAIN = 200  # for ai_query, we cannot support total_tokens yet, so set temp limit until supported

IGNORED_CACHE_ROOT = 'kie_cache_'


def cache_on_serverless(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        spark = get_spark()
        return spark.createDataFrame(result.toPandas())

    return wrapper


def cache_df(df: DataFrame, path: str) -> None:
    """Cache the dataframe at the specified path
    
    Args:
        df (DataFrame): Dataframe to be cached
        path (str): Table path at which to cache the dataframe
    """
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(path)


def get_split_from_labeled(labeled_split_df: DataFrame, split: str, request: str, expected_response: str) -> DataFrame:
    # yapf: disable
    return (labeled_split_df
            .where(F.col('split') == split)
            .withColumn('request', F.col(request))
            .withColumn('expected_response', F.col(expected_response))
    )  # yapf: enable


@cache_on_serverless
def get_split_from_unlabeled(unlabeled_split_df: DataFrame, split: str) -> DataFrame:
    df = unlabeled_split_df.where(F.col('split') == split)
    if 'request' in df.columns:
        return df
    elif 'doc_uri' in df.columns:
        return df.withColumn('request', read_document(F.col('doc_uri')))
    else:
        raise ValueError("unlabeled_split_df must have either 'doc_uri' or 'request' column")

def get_all_unlabeled(unlabeled_split_df: DataFrame) -> DataFrame:
    """Get all unlabeled data from the split df """
    if 'request' in unlabeled_split_df.columns:
        return unlabeled_split_df
    elif 'doc_uri' in unlabeled_split_df.columns:
        return unlabeled_split_df.withColumn('request', read_document(F.col('doc_uri')))
    else:
        raise ValueError("unlabeled_split_df must have either 'doc_uri' or 'request' column")

def get_valid_files(directory: str) -> List[str]:
    """ Recursively get all files in the directory that match valid extensions
    """
    all_files = []
    for root, _, files in os.walk(directory):
        if os.path.basename(root).startswith(IGNORED_CACHE_ROOT):
            # This is a cache folder - skip it
            continue
        for f in files:
            if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS:
                all_files.append(os.path.join(root, f))

    return all_files


def split_labeled_data(
    df: DataFrame,
    num_grounding_samples: int = 5,
    num_val_samples: int = 25,
    seed: int = 42,
) -> DataFrame:

    # Count the total sample size
    total_samples = df.count()

    # Allocate first to grounding, then val and training
    labeled_remaining = total_samples

    num_grounding_samples = min(num_grounding_samples, labeled_remaining)
    labeled_remaining -= num_grounding_samples

    # Default split to train
    df = df.withColumn('split', F.lit('train'))

    # Create random data splits
    # Order by rand so we can sample from it
    df = df.withColumn('rand', F.rand(seed=seed)).orderBy('rand')
    df = df.withColumn('row_id', F.row_number().over(Window.partitionBy("split").orderBy('rand')))

    # Split grounding and val data
    df = df.withColumn('split',
                       F.when(F.col('row_id') <= num_grounding_samples, F.lit('grounding')).otherwise(F.col('split')))
    df = df.withColumn('split',
                       F.when((F.col('row_id') > num_grounding_samples) & \
                              (F.col('row_id') <= num_grounding_samples + num_val_samples),
                              F.lit('val')).otherwise(F.col('split')))

    return df


def create_unlabeled_df_from_dataset(
    dataset: Optional[str],
) -> Tuple[DataFrame, List[str]]:
    all_files = get_valid_files(dataset)

    if not all_files:
        raise ValueError(f"No files found in {dataset} matching accepted file types: {','.join(VALID_EXTENSIONS)}")

    # Create a dataframe with the file paths
    spark = get_spark()
    schema = StructType([StructField('doc_uri', StringType(), True)])

    # Create DataFrame with schema
    df = spark.createDataFrame([(uri,) for uri in all_files], schema=schema).orderBy('doc_uri')
    return df, len(all_files)

def create_unlabeled_df_from_delta_table(
    delta_table: Optional[str],
    delta_table_text_column: Optional[str],
) -> Tuple[DataFrame, int]:
    spark = get_spark()
    df = (spark.read.table(delta_table)
          .select(delta_table_text_column)
          .withColumnRenamed(delta_table_text_column, 'request'))
    return df, df.count()

def split_unlabeled_data(
    dataset: Optional[str],
    delta_table: Optional[str],
    delta_table_text_column: Optional[str],
    num_val_samples: int = 25,
    num_grounding_samples: int = 5,
    seed: int = 42,
) -> DataFrame:
    if dataset:
        df, total_samples = create_unlabeled_df_from_dataset(dataset)
    elif delta_table:
        df, total_samples = create_unlabeled_df_from_delta_table(delta_table, delta_table_text_column)
    else:
        raise ValueError("Please provide one of dataset or delta_table")

    # Adjust sample counts to respect max percentages
    max_grounding = max(int(total_samples * 0.10), 1)  # 10% max for grounding
    max_val = max(int(total_samples * 0.20), 1)  # 20% max for validation

    # Calculate needed samples respecting maximums
    grounding_needed = min(num_grounding_samples, max_grounding)
    val_needed = min(num_val_samples, max_val)

    # Default split to unused
    df = df.withColumn('split', F.lit('unused'))

    # Order by rand so we can sample from it
    df = df.withColumn('rand', F.rand(seed=seed)).orderBy('rand')
    df = df.withColumn('row_id', F.row_number().over(Window.partitionBy("split").orderBy('rand')))

    # Split grounding and val data
    running_count = 0
    if grounding_needed > 0:
        df = df.withColumn('split',
                           F.when(F.col('row_id') <= grounding_needed, F.lit('grounding')).otherwise(F.col('split')))
        running_count += grounding_needed

    if val_needed > 0:
        df = df.withColumn(
            'split',
            F.when((F.col('row_id') > running_count) & (F.col('row_id') <= running_count + val_needed),
                   F.lit('val')).otherwise(F.col('split')))
        running_count += val_needed

    if dataset:
        return df.select('doc_uri', 'split').orderBy('doc_uri')
    else:
        return df.select('request', 'split')

@udf(returnType=StringType())
def read_document(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def get_fewshot_examples(
    df: DataFrame,
    num_examples: int,
    response_format: Type[BaseModel],
    response_column: str = 'expected_response',
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Extract valid few-shot examples from the provided DataFrame.

    Args:
        df: DataFrame containing request/response pairs
        num_examples: Number of examples to extract
        response_format: Expected format for validation
        response_column: Column containing the expected response

    Returns:
        List of (request, response) tuples
    """
    examples = []
    for row in df.limit(num_examples).collect():
        try:
            response = json.loads(row[response_column])
            response_format(**response)  # Validate response
            examples.append((row['request'], response))
            if len(examples) >= num_examples:
                break
        except (json.JSONDecodeError, ValidationError):
            continue
    return examples

def filter_valid_json(df: DataFrame, column_name: str, schema: Type[BaseModel]) -> DataFrame:
    spark = get_spark()

    # Convert to pandas
    pdf = df.toPandas()

    # Validate each row
    valid_mask = pdf[column_name].apply(lambda x: _is_valid_json(x, schema))

    # Filter and convert back to Spark
    filtered_pdf = pdf[valid_mask]
    return spark.createDataFrame(filtered_pdf, df.schema)

def _is_valid_json(maybe_json_str: str, schema: Type[BaseModel]) -> bool:
    try:
        schema(**json.loads(maybe_json_str))
        return True
    except:  # pylint: disable=bare-except
        return False


def _make_training_row(
    prompt: str,
    request: str,
    response: str,
) -> dict:
    user_message = prompt + '\n\nDocument:\n\n' + request.replace('"', '').replace('“', '').replace(
        '”', '') + '\n\n' + prompt
    messages = [{
        'role': 'user',
        'content': user_message
    }, {
        'role': 'assistant',
        'content': parse_json_markdown(response)
    }]
    messages_line = {'messages': messages}
    return messages_line


def process_for_sampling(df: DataFrame, seed: int = 42) -> DataFrame:
    spark = get_spark()
    df_shuffled = df.orderBy(rand(seed=seed))
    df_with_id = df_shuffled.withColumn('id', monotonically_increasing_id())
    df_with_id_static = spark.createDataFrame(df_with_id.toPandas())
    return df_with_id_static


def batched_iterator(df: DataFrame, batch_size: int = 1000) -> Iterable[pd.DataFrame]:
    current_max_index = 0
    while current_max_index < df.count():
        current_df = df.where((df.id >= current_max_index) & (df.id < current_max_index + batch_size))
        if 'request' in current_df.columns:
            yield current_df.toPandas()
        elif 'doc_uri' in current_df.columns:
            yield current_df.withColumn('request', read_document(F.col('doc_uri'))).toPandas()
        else:
            raise ValueError("df must have either 'doc_uri' or 'request' column")
        current_max_index += batch_size


def write_batch_to_cache(prompt: str,
                         documents: List[str],
                         responses: List[str],
                         response_format: Type[BaseModel],
                         file_path: str):
    lines = []
    for request, response in zip(documents, responses):
        if not _is_valid_json(response, response_format):
            continue

        training_row = _make_training_row(
            prompt=prompt,
            request=request,
            response=response,
        )
        lines.append(json.dumps(training_row))

    with open(file_path, 'a', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n' if lines else '')



def create_training_data(
    unlabeled_split_df: DataFrame,
    prompt: str,
    response_format: Type[BaseModel],
    train_jsonl_cache_path: str,
    endpoint: BaseEndpoint,
    token_budget: int,
    min_docs_to_train: int = MIN_DOCS_TO_TRAIN,
    use_ai_query: bool = False,
) -> Optional[Tuple[str, int]]:

    train_df = unlabeled_split_df.where((F.col('split') == 'train') | (F.col('split') == 'unused'))

    if train_df.count() < min_docs_to_train:
        return None

    if use_ai_query:
        # Read training documents into the table and save it out
        train_df = get_all_unlabeled(train_df.limit(MAX_DOCS_TO_TRAIN))

        # Write to temporary view
        train_df.createOrReplaceTempView("train_df")

        result_df = endpoint.generate_ai_query(
            data_path="train_df",
            system_prompt=prompt,
            response_format=response_format,
        )
        print(f"Finished generating {result_df.count()} responses from ai_query")
        # Write to train_jsonl_cache_path
        result_df.toPandas().to_json(train_jsonl_cache_path,
          orient='records',
          lines=True)
        # Note that we don't have support for token budget yet, so we are just returning 0
        return train_jsonl_cache_path, 0

    ready_for_sampling = process_for_sampling(train_df)

    with tempfile.NamedTemporaryFile(mode='w', delete=True) as temp_file:
        # Create a temp file to write to since UC Volumes don't allow appending to files
        temp_path = temp_file.name
        token_budget_remaining = token_budget
        for batch in batched_iterator(ready_for_sampling):
            documents = batch['request'].tolist()

            responses = endpoint.generate_batch(
                prompts=documents,
                system_prompt=prompt,
                total_max_tokens=token_budget_remaining,
                response_format=response_format,
                show_progress=False,
            )

            actual_responses = [r.response for r in responses]

            write_batch_to_cache(prompt, documents, actual_responses, response_format, temp_path)
            token_budget_remaining -= sum(r.total_tokens for r in responses)

        # Copy the temp file to the final location
        # Must use a copy and not a move on serverless due to permissions issues
        shutil.copyfile(temp_path, train_jsonl_cache_path)
    return train_jsonl_cache_path, token_budget - token_budget_remaining


def validate_row_count(
    df: DataFrame,
    required_count: int = 10,
    recommended_count: int = 1000,
) -> None:
    row_count = df.count()
    if row_count < required_count:
        raise ValueError(f'Insufficient data. Found {row_count} rows, expected at least {required_count}.')
    if row_count < recommended_count:
        print(f'Warning: Found {row_count} rows, recommended at least {recommended_count} for best results.')


def to_row_based_format(column_based_data: Dict[str, List[str]]) -> List[Dict[str, str]]:
    """
    Converts column-based data to row-based format.

    Args:
        column_based_data (dict): A dictionary where keys are column names and values are lists of column values.

    Returns:
        list: A list of dictionaries where each dictionary represents a row of data.
    """
    row_based_data = []
    num_rows = len(next(iter(column_based_data.values())))

    if len(set(len(values) for values in column_based_data.items())) != 1:
        raise ValueError('column-based data must have the same number of rows for all columns')

    for i in range(num_rows):
        row = {key: value[i] for key, value in column_based_data.items()}
        row_based_data.append(row)
    return row_based_data


def to_column_based_format(row_based_data: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Converts row-based data to column-based format.

    Args:
        row_based_data (list): A list of dictionaries where each dictionary represents a row of data.

    Returns:
        dict: A dictionary where keys are column names and values are lists of column values.
    """
    if not row_based_data:
        return {}

    column_based_data = {key: [] for key in row_based_data[0].keys()}
    for row in row_based_data:
        if set(row.keys()) != set(column_based_data.keys()):
            raise ValueError('all rows must have the same keys')

        for key, value in row.items():
            column_based_data[key].append(value)
    return column_based_data


def read_from_table_with_columns(
    table_path: str,
    columns: Tuple[str],
    count: int,
    filter_null_value: bool = False,
) -> List[Dict[str, Any]]:
    """
    Reads specified columns from a table and returns a DataFrame with a limited number of rows.

    Args:
        table_path (str): The path to the table.
        columns (List[str]): The list of columns to read.
        count (int): The number of rows to read.
        filter_null_value (bool): Whether to filter out rows with null values in the specified columns.

    Returns:
        list: A list of dictionaries where each dictionary represents a row of the DataFrame.
    """
    if not check_if_table_exists(table_path):
        raise ValueError(f'{table_path} is not a valid table path. Please check that your table exists.')
    if not check_table_has_columns(table_path, columns):
        raise ValueError(f'{table_path} does not have expected columns: {columns}')

    spark = get_spark()
    df = spark.read.table(table_path).select(*columns)
    if filter_null_value:
        df = df.filter(" AND ".join(f"{col} IS NOT NULL" for col in columns))
    df = df.limit(count).collect()

    return [datum.asDict() for datum in df]

def read_from_jsonl(file_path: str, count: Optional[int]= None) -> List[Dict[str, Any]]:
    """
    Reads a JSONL file and returns a specified number of rows.

    Args:
        file_path (str): The path to the JSONL file.
        count (int): Optional number of rows to read.

    Returns:
        list: A list of dictionaries where each dictionary represents a row of the JSONL file.
    """
    json_obj = pd.read_json(path_or_buf=file_path, lines=True, nrows=count)
    return json_obj.to_dict(orient='records') # pylint: disable=no-member

def partition_data(
    data: List[Any],
    min_test_data_size: int = 10,
    test_set_ratio: float = 0.5,
) -> Tuple[List[Any], List[Any]]:
    """Randomly split data to test data and train data."""
    data_to_partition = deepcopy(data)
    example_data_size = len(data_to_partition)
    if example_data_size <= min_test_data_size:
        return [], data_to_partition

    random.shuffle(data_to_partition)
    split_index = int(example_data_size * test_set_ratio)
    return data_to_partition[split_index:], data_to_partition[:split_index]
