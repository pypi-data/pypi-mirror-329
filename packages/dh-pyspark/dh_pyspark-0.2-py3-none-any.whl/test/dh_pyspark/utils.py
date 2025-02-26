import datetime
import math

import pyspark.sql.functions as f
from dh_pyspark.common.utills import create_data_frame
from pyspark.sql import DataFrame

from dataheroes.data.common import DataParams

from dh_pyspark.model.tree_model import TreeDataFrame
from dh_pyspark.services._coreset_service_base import CoresetTreeServiceBase, SUB_CHUNK_PREFIX


def delete_all_files(path):
    import shutil
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f'Failed to delete directory: {e}')


def print_tree(coreset_tree: TreeDataFrame, number_rows, column_list=None):
    # coreset_tree= dict(sorted(coreset_tree.items()))

    if column_list is None:
        column_list = ["*"]

    for level in coreset_tree.tree_ldf:
        print(f"the coreset date on level {level.level}")
        level.level_df.select(column_list).orderBy("chunk_index").show(n=number_rows, truncate=False)

    print(f"the coreset date for validation")
    coreset_tree.getValidationDF().select(column_list).orderBy("chunk_index").show(n=number_rows,
                                                                                   truncate=False)


def check_tree(coreset_tree: TreeDataFrame, df: DataFrame, chunk_size, leaf_factor=2, start_row_index=1, chunk_by=None,
               partial_build=False, service: CoresetTreeServiceBase = None):
    """
        Used in pytests to validate the structure and properties of a coreset tree against given parameters and data.

        This function performs extensive validation of a coreset tree, including:
        - Tree size and level calculations
        - Chunk size verification
        - Data distribution across chunks
        - Date range validations for temporal data in case of chunk by

        Args:
            coreset_tree (TreeDataFrame): The tree structure to validate
            df (DataFrame): Input DataFrame containing the original data
            chunk_size (int): Size of each chunk (number of rows)
            leaf_factor (int, optional): Maximum number of children per node. Defaults to 2
            start_row_index (int, optional): Starting index for row numbering. Defaults to 1
            chunk_by (str, optional): Column name used for chunking. Defaults to None
            partial_build (bool, optional): Whether tree is partially built. Defaults to False
            service (CoresetTreeServiceBase, optional): Service object for tree operations

        Raises:
            AssertionError: If any validation check fails
        """
    data_size = df.count()
    # Calculate maximum number of chunks based on chunk size or chunk_by column
    if chunk_size is not None and chunk_size > 0:
        max_chunk = (data_size + chunk_size - 1) // chunk_size
        if partial_build:
            max_chunk = max_chunk + coreset_tree.tree_params.first_level_last_max_chunk

    if chunk_by is not None:
        if chunk_size is not None:
            df = service._create_chunk_by_sub_chunks(chunk_by, chunk_size, df)
        max_chunk = df.select(chunk_by).distinct().count()
        if partial_build:
            max_chunk = max_chunk + coreset_tree.tree_params.first_level_last_max_chunk

    validation_max_chunk = max_chunk
    tree_size = coreset_tree.getTreeSize()
    level = 0
    assert tree_size >= 0, "Tree size is less then 0"
    while max_chunk > leaf_factor - 1:
        level += 1
        max_chunk = math.floor(max_chunk / leaf_factor)
    level_ = level + 1
    assert tree_size == level_, f"Tree size vs calculated not equal tree size {tree_size} calculated size is {level}"

    assert coreset_tree.getChunkDataNoCoresetDF().agg({f"chunk_index": "max"}).collect()[0][
               0] == validation_max_chunk, f"max chunk is not {validation_max_chunk} in data no coreset ןit"
    if chunk_by is None:
        is_no_mod = data_size % chunk_size == 0

        if partial_build:
            index__count__collect = coreset_tree.getChunkDataNoCoresetDF().where(
                f.col("chunk_index") > coreset_tree.tree_params.first_level_last_max_chunk).groupBy(
                "chunk_index").count().collect()
        else:
            index__count__collect = coreset_tree.getChunkDataNoCoresetDF().groupBy("chunk_index").count().collect()

        chunk_index_size_dict = [row.asDict() for row in index__count__collect]
        print(chunk_index_size_dict)
        # validate chunk size for each chunk.
        for item in chunk_index_size_dict:

            if item["chunk_index"] == validation_max_chunk and is_no_mod == False:
                assert item[
                           "count"] < chunk_size, f"chunk index {item['chunk_index']}  is not less then size {chunk_size} is partial build {partial_build}."
            else:
                assert item[
                           "count"] == chunk_size, f"chunk index {item['chunk_index']}  is not equal to size {chunk_size} is partial build {partial_build}."

    # Validate maximum chunk index in validation data which
    assert coreset_tree.getValidationDF().agg({f"chunk_index": "max"}).collect()[0][
               0] == validation_max_chunk, f"max chunk is not {validation_max_chunk} in validation"
    last_level_chunk_index = \
        coreset_tree.getLevelDF(coreset_tree.getTreeSize() - 1).agg({f"chunk_index": "max"}).collect()[0][0]
    assert last_level_chunk_index <= leaf_factor - 1 and last_level_chunk_index > 0, \
        (f"last level chunk index is incorrect - {last_level_chunk_index} "
         f"value should be greater then 0 and smaller then {leaf_factor - 1}")
    # Additional validations for column-based chunking
    if chunk_by is not None:
        def format_date(date, d_format):
            if isinstance(date, str):
                date = date.split(SUB_CHUNK_PREFIX)[0]
                date = datetime.datetime.strptime(date, d_format)
            return date

        datetime_format_ = service._tree_params.data_params.seq_column["datetime_format"]

        chunk_by_tree = service._tree_params.chunk_by_tree
        no_coreset_df = coreset_tree.getChunkDataNoCoresetDF().select(chunk_by).orderBy("chunk_index")
        first_date = no_coreset_df.head(1)[0][0]
        first_date = format_date(first_date, datetime_format_)
        last_date = no_coreset_df.tail(1)[0][0]
        last_date = format_date(last_date, datetime_format_)

        assert len(chunk_by_tree) == coreset_tree.getTreeSize()
        # Validate date ranges at each level
        level = 0
        for chunk_by_level in chunk_by_tree:
            level_df = coreset_tree.getLevelDF(level)
            # this test can change depending on coreset size
            # assert level_df.select("chunk_index").distinct().count() == len(chunk_by_level)
            for i, chunk in chunk_by_level.iterrows():
                collect = level_df.where(level_df["chunk_index"] == chunk["chunk_index"]).agg(f.min(chunk_by),
                                                                                              f.max(chunk_by)).collect()
                start_date = collect[0][0]
                start_date = format_date(start_date, datetime_format_)
                end_date = collect[0][1]
                end_date = format_date(end_date, datetime_format_)
                if level == 0:  # in level 0 all dates should be there
                    if i == 0:
                        assert first_date == chunk["start_seq"]
                    if i == len(chunk_by_level) - 1:
                        assert last_date == chunk["start_seq"]
                    assert start_date == chunk["start_seq"]
                    assert end_date == chunk["end_seq"]
                else:  # in tasting the coreset size can change and not all dates can be present after calculating coreset
                    assert start_date >= chunk["start_seq"]
                    assert end_date <= chunk["end_seq"]
            level += 1


def get_dataset(spark, numeric_only: bool, missing_values: bool):
    # Sample data: Create a DataFrame with "features " and "y values" columns
    number_of_features = 2
    number_of_rows = 100
    if numeric_only:
        categorical_features = []
    else:
        categorical_features = [['A', 'B', 'C'], ['K', 'N']]
    df, _ = create_data_frame(number_of_features, categorical_features, number_of_rows, spark, missing_values)
    if not numeric_only:
        data_params = DataParams.from_dict({
            'features': [
                {'name': 'f0', 'categorical': True},
                {'name': 'f1', 'categorical': True},
                {'name': 'f2'},
                {'name': 'f3'},
            ],
            'target': {'name': 'y'},
            'fill_value_cat': 'NNN',
            'fill_value_num': 0,
        })
    else:
        data_params = DataParams.from_dict({
            'features': [
                {'name': 'f0'},
                {'name': 'f1'},
            ],
            'target': {'name': 'y'},
            'fill_value_num': 0,
        })
    return df, data_params
