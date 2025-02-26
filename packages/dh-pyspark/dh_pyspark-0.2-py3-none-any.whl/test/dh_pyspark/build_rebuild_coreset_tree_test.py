import datetime
import os

import numpy as np
import pytest
from dataheroes.data.common import DataParams

from dh_pyspark.common.utills import create_data_frame, create_large_simple_data_rdd, \
    create_random_dataframe_start_end_date, create_large_simple_date_data
from dh_pyspark.services._coreset_service_base import DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES
from dh_pyspark.services.coreset.dtc import CoresetTreeServiceDTC
from test.dh_pyspark.utils import delete_all_files, print_tree, check_tree

test_output_folder = "test_output"

DATA_PARAMS_CAT = DataParams.from_dict({
    'features': [
        {
            'name': 'f0',
            'categorical': True, 'fill_value': 'C'
        },
        {'name': 'f1', 'categorical': True},
        {'name': 'f2', 'fill_value': "mean"},
        {'name': 'f3'},

    ],
    'target': {'name': 'y'},
    'fill_value_cat': 'NNN',
    'fill_value_num': 0,
})
DATA_PARAMS_CAT_CHUNK_BY = DataParams.from_dict({
    'features': [
        {
            'name': 'f0',
            'categorical': True, 'fill_value': 'C'
        },
        {'name': 'f1', 'categorical': True},
        {'name': 'f2', 'fill_value': "mean"},
        {'name': 'f3'},

    ],
    'target': {'name': 'y'},
    'fill_value_cat': 'NNN',
    'fill_value_num': 0,
    'seq_column':
        {
            'name': 'date',
            'granularity': 'D',
            'datetime_format': '%Y-%m-%d',
            'chunk_by': True
        },

})

plain_data_param_dic = {
    'features': list(({"name": f"f{i}"} for i in range(1, 5))),
    'target': {'name': 'y'},
}
plain_data_param_chunk_by_dic = {
    'features': list(({"name": f"f{i}"} for i in range(1, 5))),
    'target': {'name': 'y'},
    'fill_value_num': 0,
    'seq_column':
        {
            'name': 'date',
            'granularity': 'D',
            'datetime_format': '%Y-%m-%d',
            'chunk_by': True
        },
}
DATA_PARAMS_PLAIN = DataParams.from_dict(plain_data_param_dic)
DATA_PARAMS_PLAIN_CHUNK_BY = DataParams.from_dict(plain_data_param_chunk_by_dic)


def test_build_by_column_random(spark):
    """
    Test build chunk by column (date) random data
    """
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[1])
    row_number = 211
    chunk_size = 20
    data_params = {
        'features': list(({"name": f"f{i}"} for i in range(2, 4))),
        'target': {'name': 'y'},
        'fill_value_num': 0,
        'seq_column':
            {
                'name': 'date',
                'granularity': 'D',
                'datetime_format': '%Y-%m-%d %H:%M:%S',
                'chunk_by': True
            },
    }

    df, _ = create_large_simple_data_rdd(
        spark=spark, base_number=row_number, column_numbers=5, target_column_name="y", target_column_number=0,
        power_number=1, date_column_number=1, starting_month=4, starting_year=2024, ending_month=4)
    df.show(n=50)
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    chunk_sample_ratio = 0.9
    coreset_size = 1.0
    chunk_by = "date"

    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, chunk_sample_ratio=chunk_sample_ratio, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size, chunk_by=chunk_by, service=service)
    print_tree(coreset_tree, row_number)
    assert os.path.exists(os.path.join(indexer_meth_data_path, "logs/udf_create_coreset.log"))


def test_build_by_column_random_hourly(spark):
    """
    Test build chunk by column (date) chunk data hourly date format with specified chunk size
    """
    row_number = 20
    chunk_size = int(row_number / 5)
    date_format = '%Y-%m-%d %H:%M:%S'
    data_params = {
        'features': list(({"name": f"f{i}"} for i in range(2, 4))),
        'target': {'name': 'y'},
        'fill_value_num': 0,
        'seq_column':
            {
                'name': 'date',
                'granularity': 'H',
                'datetime_format': date_format,
                'chunk_by': True
            },
    }

    df = create_random_dataframe_start_end_date(spark=spark, start_date='2024-04-01 08:30:00',
                                                end_date='2024-04-03 08:30:00', num_columns=5, num_rows=row_number,
                                                date_format=date_format, granularity="H")
    df.show(n=row_number)
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    chunk_sample_ratio = 0.9
    coreset_size = 0.2
    chunk_by = "date"

    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, chunk_sample_ratio=chunk_sample_ratio, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size, chunk_by=chunk_by, service=service)
    print_tree(coreset_tree, row_number)
    assert not os.path.exists(os.path.join(indexer_meth_data_path, "logs/udf_create_coreset.log"))


def test_build_by_column_random_hourly_no_chunk(spark):
    """
    Test build chunk by column (date) chunk data hourly date format with no chunk size
    """
    row_number = 50
    chunk_size = None
    date_format = '%Y-%m-%d %H:%M:%S'
    data_params = {
        'features': list(({"name": f"f{i}"} for i in range(2, 4))),
        'target': {'name': 'y'},
        'fill_value_num': 0,
        'seq_column':
            {
                'name': 'date',
                'granularity': 'H',
                'datetime_format': date_format,
                'chunk_by': True
            },
    }

    df = create_random_dataframe_start_end_date(spark=spark, start_date='2024-04-01 08:30:00',
                                                end_date='2024-04-03 08:30:00', num_columns=5, num_rows=row_number,
                                                date_format=date_format, granularity="H")
    df.show(n=row_number)
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    chunk_sample_ratio = 0.9
    coreset_size = 0.2
    chunk_by = "date"

    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, chunk_sample_ratio=chunk_sample_ratio, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)

    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    print_tree(coreset_tree, row_number)
    check_tree(coreset_tree, df, chunk_size, chunk_by=chunk_by, service=service)


def test_build_partial_build_by_column(spark):
    """
    Test chunk by column (date) build and partial build with chunk size
    """
    number_features = 6
    chunk_size = 25

    number_rows = 500
    df, f_arr = create_data_frame(number_features, None, number_rows, spark, True, 50)
    df.show()
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    # chunk_sample_ratio = 0.6
    coreset_size = 0.2

    data_params = DATA_PARAMS_PLAIN_CHUNK_BY
    chunk_by = "date"
    column_display_list = [chunk_by, "chunk_index"]
    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, data_params=data_params, n_instances=number_rows,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size, chunk_by=chunk_by, service=service)
    print_tree(coreset_tree, number_rows, column_display_list)
    new_number_rows = 100
    new_df, f_arr = create_data_frame(number_features, None, new_number_rows, spark, True, 50,
                                      datetime.datetime.now() + datetime.timedelta(days=50))
    new_df2, f_arr = create_data_frame(number_features, None, new_number_rows, spark, True, 50,
                                       datetime.datetime.now() + datetime.timedelta(days=100))
    # new_df.show(n=new_number_rows)
    service2 = CoresetTreeServiceDTC(dhspark_path=indexer_meth_data_path, n_instances=new_number_rows)
    service2.partial_build_preprocess_from_df(spark_session=spark, input_df=new_df)
    service2.partial_build(spark_session=spark)
    coreset_tree = service2._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, new_df, chunk_size, chunk_by=chunk_by, partial_build=True, service=service2)
    service2.partial_build_preprocess_from_df(spark_session=spark, input_df=new_df2)
    service2.partial_build(spark_session=spark)
    coreset_tree = service2._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, new_df2, chunk_size, chunk_by=chunk_by, partial_build=True, service=service2)
    # print_tree(coreset_tree, number_rows + new_number_rows, column_display_list)


def test_build_partial_build_by_column_category(spark):
    """
    Test chunk by column (date) build and partial build with chunk size with categorical features
    """
    number_features = 2
    chunk_size = 3

    categorical_features = [['A', 'B', 'C'], ["F", "G"]]
    number_rows = 200
    df, f_arr = create_data_frame(number_features, categorical_features, number_rows, spark, True, 10)
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)

    coreset_size = 0.2

    data_params = DATA_PARAMS_CAT_CHUNK_BY
    chunk_by = "date"
    column_display_list = [chunk_by, "chunk_index"]
    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, n_instances=number_rows, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size, chunk_by=chunk_by, service=service)
    print_tree(coreset_tree, number_rows, column_display_list)
    new_number_rows = 40
    new_df, f_arr = create_data_frame(number_features, categorical_features, new_number_rows, spark, True, 10,
                                      datetime.datetime.now() + datetime.timedelta(days=50))
    new_df2, f_arr = create_data_frame(number_features, categorical_features, new_number_rows, spark, True, 10,
                                       datetime.datetime.now() + datetime.timedelta(days=100))
    new_df.show(n=new_number_rows)
    service2 = CoresetTreeServiceDTC(dhspark_path=indexer_meth_data_path)
    service2.partial_build_preprocess_from_df(spark_session=spark, input_df=new_df)
    service2.partial_build(spark_session=spark)
    coreset_tree = service2._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, new_df, chunk_size, chunk_by=chunk_by, partial_build=True, service=service2)
    service2.partial_build_preprocess_from_df(spark_session=spark, input_df=new_df2)
    service2.partial_build(spark_session=spark)
    coreset_tree = service2._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, new_df2, chunk_size, chunk_by=chunk_by, partial_build=True, service=service2)
    print_tree(coreset_tree, number_rows + new_number_rows, column_display_list)


def test_build_partial_build_coreset_tree_with_instances(spark):
    """
    Test  build and partial build where the exact n instance (row number) is given
    """
    instances = 211
    chunk_size = 30
    df, _ = create_large_simple_data_rdd(
        spark=spark, base_number=instances, column_numbers=5, target_column_name="y", target_column_number=0,
        power_number=1)
    meth_data_path = test_output_folder
    delete_all_files(meth_data_path)
    data_params = DATA_PARAMS_PLAIN
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2, data_params=data_params,
        dhspark_path=meth_data_path, n_instances=instances, n_instances_exact=True)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=meth_data_path)
    check_tree(tree, df, chunk_size)
    column_display_list = ["row_index_id", "chunk_index", "level"]
    print_tree(tree, instances, column_list=column_display_list)
    service2 = CoresetTreeServiceDTC(dhspark_path=meth_data_path, n_instances=instances, n_instances_exact=True)
    service2.partial_build_preprocess_from_df(spark_session=spark, input_df=df)
    service2.partial_build(spark_session=spark)
    tree = service2._load(spark=spark, dhspark_path=meth_data_path)
    print_tree(tree, instances, column_list=column_display_list)
    check_tree(tree, df, chunk_size, partial_build=True)
    # column_display_list = ["row_index_id", "chunk_index", "level"]
    # print_tree(tree, instances, column_list=column_display_list)


def test_build_coreset_tree_with_instances(spark):
    """
    Test  build where the exact n instance (row number) is given
    """

    instances = 21
    df, _ = create_large_simple_data_rdd(
        spark=spark, base_number=instances, column_numbers=5, target_column_name="y", target_column_number=0,
        power_number=1)

    chunk_size = 4
    print(chunk_size)
    meth_data_path = test_output_folder
    delete_all_files(meth_data_path)
    data_params = DATA_PARAMS_PLAIN
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2, data_params=data_params,
        dhspark_path=meth_data_path, n_instances=instances)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=meth_data_path)
    check_tree(tree, df, chunk_size)
    print_tree(tree, int(instances / 100))


def test_create_coreset_tree_7_merge_factor(spark):
    """
    Test  build where the coreset tree is not binary (merge factor is 2) changing it to 7
    """
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=415, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    chunk_size = 20
    leaf_factor = 7
    print(chunk_size)

    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    data_params = DATA_PARAMS_PLAIN

    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2, chunk_sample_ratio=0.4, data_params=data_params,
        dhspark_path=indexer_meth_data_path)
    service._tree_params.leaf_factor = leaf_factor
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)

    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    print_tree(coreset_tree, 450)

    check_tree(coreset_tree, df, chunk_size, leaf_factor)


def test_create_min_max_chunk_by_coreset_tree(spark):
    """
    Test  build chunk by tree where the data to build the tree is created using create_large_simple_date_data which can
     get a max and min rows per date and created chunk by date according to that
    """
    delete_all_files(test_output_folder)

    total_rows = 1000
    column_numbers = 5
    target_column_name = "y"
    target_column_number = 0
    date_column_number = 1
    date_column_name = "date"
    starting_month = 3
    ending_month = 4
    starting_year = 2024
    max_rows_per_day = 30
    min_rows_per_day = 10
    data_params = {
        'features': list(({"name": f"f{i}"} for i in range(column_numbers - 3, column_numbers - 1))),
        'target': {'name': 'y'},
        'fill_value_num': 0,
        'seq_column':
            {
                'name': date_column_name,
                'granularity': 'D',
                'datetime_format': '%Y-%m-%d %H:%M:%S',
                'chunk_by': True
            },
    }

    spark.conf.set("spark.sql.shuffle.partitions", 200)

    df, path = create_large_simple_date_data(
        spark, total_rows, column_numbers, target_column_name, target_column_number,
        date_column_number, date_column_name, starting_month, starting_year,
        ending_month, max_rows_per_day, min_rows_per_day
    )
    df.show()
    chunk_size = int(max_rows_per_day + min_rows_per_day / 2)
    service = CoresetTreeServiceDTC(
        coreset_size=0.2, chunk_sample_ratio=0.4, data_params=data_params,
        dhspark_path=test_output_folder, chunk_by=date_column_name, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df, chunk_size, chunk_by=date_column_name, service=service)


def test_create_coreset_tree(spark):
    """
    Test build a simple coreset tree and checking it.
    """
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=1000, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)

    chunk_size = 100
    leaf_factor = 2
    print(chunk_size)

    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)

    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2, chunk_sample_ratio=0.4, data_params=plain_data_param_dic,
        dhspark_path=indexer_meth_data_path)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)

    check_tree(coreset_tree, df, chunk_size, leaf_factor)


def test_create_coreset_save_stop_level(spark):
    """
    Test build coreset with stop_level  the stop level can control the building of the tree app to spastic level
    is used to create the tree in multi session separation.
    """

    df, _ = create_large_simple_data_rdd(spark=spark, base_number=210, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)

    chunk_size = 20
    leaf_factor = 2
    print(chunk_size)

    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    data_params = DATA_PARAMS_PLAIN

    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.2, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=indexer_meth_data_path
                                    )
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark, stop_level=0)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    assert coreset_tree.getTreeSize() == 1
    service.build(spark_session=spark, stop_level=2)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    assert coreset_tree.getTreeSize() == 3
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size, leaf_factor)


def test_create_coreset_partial_build_stop_level(spark):
    """
    Test build and partial build coreset with stop_level  the stop level can control the building of the tree app to spastic level
    is used to create the tree in multi session separation.
    """

    df, _ = create_large_simple_data_rdd(spark=spark, base_number=210, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)

    chunk_size = 20

    print(chunk_size)

    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    data_params = DATA_PARAMS_PLAIN
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.2, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=indexer_meth_data_path
                                    )
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size)
    new_df, _ = create_large_simple_data_rdd(spark=spark, base_number=80, column_numbers=5, target_column_name="y",
                                             target_column_number=0, power_number=1)

    service.partial_build_preprocess_from_df(spark_session=spark, input_df=new_df)
    service.partial_build(spark_session=spark, stop_level=0)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    assert coreset_tree.tree_params.stop_level == 0
    assert coreset_tree.tree_params.stop_tree_size == 1
    service.partial_build(spark_session=spark, stop_level=1)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    assert coreset_tree.tree_params.stop_level == 1
    assert coreset_tree.tree_params.stop_tree_size == 2
    service.partial_build(spark_session=spark, stop_level=2)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    assert coreset_tree.tree_params.stop_level == 2
    assert coreset_tree.tree_params.stop_tree_size == 3
    service.partial_build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    assert coreset_tree.tree_params.stop_level is None
    assert coreset_tree.tree_params.stop_tree_size is None
    check_tree(coreset_tree, new_df, chunk_size, partial_build=True)


def test_build_partial_build_tree(spark):
    """
    Test build and partial build with categorical features with multipule DTC services
    """
    # Sample data: Create a DataFrame with "features " and "y values" columns
    marge_factore = 2
    number_features = 2
    categorical_features = [['A', 'B', 'C'], ['K', 'N']]
    number_rows = 183
    categorical_columns_names_values = {"f0": "A", "f1": "K"}
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    chunk_size = 20
    chunk_sample_ratio = 0.8
    coreset_size = 0.8
    column_display_list = ["row_index_id", "chunk_index"]
    df, f_arr = create_data_frame(number_features, categorical_features, number_rows, spark, True)
    print("data frame with missing data")
    df.show(n=number_rows)
    data_params = DATA_PARAMS_CAT
    print("the data before adding coreset logic and metadata")
    print(
        f"the categorical features columns names : {categorical_columns_names_values} passable values are: {categorical_features} number of rows {number_rows}")

    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=coreset_size,
                                    chunk_sample_ratio=chunk_sample_ratio,
                                    data_params=data_params,
                                    dhspark_path=indexer_meth_data_path
                                    )
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size, marge_factore)
    print("tree before partial build")
    print_tree(coreset_tree, number_rows, column_display_list)
    new_row_size = 90
    categorical_features_new = [['B', 'C', 'G', 'L'], ['K', 'N', "M"]]
    new_df, _ = create_data_frame(number_features, categorical_features_new, new_row_size, spark)
    print("the new data  to add before adding coreset")
    new_df.show(n=100)
    service2 = CoresetTreeServiceDTC(dhspark_path=indexer_meth_data_path)
    service2.partial_build_preprocess_from_df(spark_session=spark, input_df=new_df)
    service2.partial_build(spark_session=spark)
    coreset_tree = service._load(spark, indexer_meth_data_path)
    check_tree(coreset_tree, new_df, chunk_size, marge_factore, partial_build=True)
    print("tree after partial build")
    print_tree(coreset_tree, 2 * number_rows, column_display_list)


def test_build_partial_build_from_file(spark):
    """
    Test build and partial build from a parquet file
    """

    chunk_size = 20
    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=100, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    df2, _ = create_large_simple_data_rdd(spark=spark, base_number=50, column_numbers=5, target_column_name="y",
                                          target_column_number=0, power_number=1)
    build_input_path = os.path.join(test_output_folder, "build_input")
    df.write.parquet(build_input_path)
    partial_input_path = os.path.join(test_output_folder, "partial_input")
    df2.write.parquet(partial_input_path)
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.8, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=test_output_folder)
    service.build_preprocess_from_file(spark_session=spark, input_path=build_input_path)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df, chunk_size)
    service.partial_build_preprocess_from_file(spark_session=spark, input_path=partial_input_path)
    service.partial_build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df.union(df2), chunk_size)


def test_build_partial_build_save_mode_index(spark):
    """
    Test build and partial build with save mode 3 (CALCULATED_COLUMNS_NO_INDEX) only calculated fields.
    """

    chunk_size = 20
    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=100, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    df2, _ = create_large_simple_data_rdd(spark=spark, base_number=50, column_numbers=5, target_column_name="y",
                                          target_column_number=0, power_number=1)

    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.8, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=test_output_folder
                                    )
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df, chunk_size)
    service.partial_build_preprocess_from_df(spark_session=spark, input_df=df2)
    service.partial_build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df.union(df2), chunk_size)


def test_build_partial_build_from_file_json(spark):
    """
    Test build and partial build from a json file
    """
    chunk_size = 20
    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=100, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    df2, _ = create_large_simple_data_rdd(spark=spark, base_number=50, column_numbers=5, target_column_name="y",
                                          target_column_number=0, power_number=1)
    build_input_path = os.path.join(test_output_folder, "build_input")
    df.write.json(build_input_path)
    partial_input_path = os.path.join(test_output_folder, "partial_input")
    df2.write.json(partial_input_path)
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.8, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=test_output_folder)
    service.build_preprocess_from_file(spark_session=spark, input_path=build_input_path, input_format="json")
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df, chunk_size)
    service.partial_build_preprocess_from_file(spark_session=spark, input_path=partial_input_path, input_format="json")
    service.partial_build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df.union(df2), chunk_size)


def test_build_partial_build_from_file_csv(spark):
    """
    Test build and partial build from a csv file
    """

    chunk_size = 20
    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=100, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    df2, _ = create_large_simple_data_rdd(spark=spark, base_number=50, column_numbers=5, target_column_name="y",
                                          target_column_number=0, power_number=1)
    build_input_path = os.path.join(test_output_folder, "build_input")
    df.write.option("header", "true").csv(build_input_path)
    partial_input_path = os.path.join(test_output_folder, "partial_input")
    df2.write.option("header", "true").csv(partial_input_path)
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.8, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=test_output_folder)
    service.build_preprocess_from_file(spark_session=spark, input_path=build_input_path, input_format="csv")
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df, chunk_size)
    service.partial_build_preprocess_from_file(spark_session=spark, input_path=partial_input_path, input_format="csv")
    service.partial_build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=test_output_folder)
    check_tree(coreset_tree, df.union(df2), chunk_size)


def test_n_time_partial_build(spark):
    """
    Test partial build coreset n times (4) in arrow .
    """

    df, _ = create_large_simple_data_rdd(spark=spark, base_number=77, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    n = 4
    chunk_size = 20

    print(chunk_size)

    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    data_params = DATA_PARAMS_PLAIN
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.8, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=indexer_meth_data_path)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark, stop_level=0)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    check_tree(coreset_tree, df, chunk_size)

    for i in range(n):
        service.partial_build_preprocess_from_df(spark_session=spark, input_df=df)
        service.partial_build(spark_session=spark, stop_level=0)
        service.partial_build(spark_session=spark)
        coreset_tree = service._load(spark, indexer_meth_data_path)
        check_tree(coreset_tree=coreset_tree, df=df, chunk_size=chunk_size, partial_build=True)


@pytest.mark.parametrize('n_instances_ratio', [
    (1350_000_000, 0.01, 0.001),  # Very large dataset with 1% target ratio
    (1000, 1.0, 0.1),  # Small dataset with 100% target ratio
    (2_000_000, 0.2, 0.02),  # Medium dataset with 20% target ratio
    (17_000_000, 0.1, 0.01),  # Large dataset with 10% target ratio
    (350_000_000, 0.05, 0.005),  # Very large dataset with 5% target ratio
    (None, 0.05, 0.005)  # Test case with no instance limit
])
def test_sample_ratio_with_instancess(spark, n_instances_ratio):
    """
       Tests the sampling ratio functionality of CoresetTreeService with various dataset sizes.

       This test verifies that the validation set size falls within expected bounds based on
       the specified sampling ratio and tolerance. It tests different scenarios from very small
       to very large datasets.
    """

    df, _ = create_large_simple_data_rdd(spark=spark, base_number=10000, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    chunk_size = 100

    print(chunk_size)

    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2,
        n_instances=n_instances_ratio[0],
        data_params=data_params,
        dhspark_path=test_output_folder)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=test_output_folder)
    ## Calculate expected bounds for validation set size
    # Since in spark sampleBy function do not inshure min and max rows i added a treshhould of a small presantage over and under the sample ratio value.
    min = (n_instances_ratio[1] - n_instances_ratio[2]) * tree.getChunkDataNoCoresetDF().count()
    max = (n_instances_ratio[1] + n_instances_ratio[2]) * tree.getChunkDataNoCoresetDF().count()
    validation_count = tree.getValidationDF().count()
    assert max >= validation_count >= min


def test_sample_ratio_equal_zero(spark):
    """
    if chunk_sample_ratio==0 we should not create validation data, let's check it
    """
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=210, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    chunk_size = 20

    print(chunk_size)

    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2,
        chunk_sample_ratio=0.0,  # initially set 0.0! should not create validation data
        data_params=data_params,
        dhspark_path=test_output_folder)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=test_output_folder)
    assert tree.getValidationDF() is None


def test_int_coreset_size(spark):
    """
    integer coreset_size, instead of ratio - number of samples
    """
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=210, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    chunk_size = 20

    print(chunk_size)

    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    coreset_size_int = 10
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=coreset_size_int,
        chunk_sample_ratio=0.0,
        data_params=data_params,
        dhspark_path=test_output_folder)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=test_output_folder)
    for level in tree.tree_ldf:
        chunk_indexes = level.level_df.select('chunk_index').toPandas().to_numpy()
        # check that node sizes do not exceed coreset_size (passed as integer)
        assert np.unique(chunk_indexes, return_counts=True)[1].max() <= coreset_size_int


def test_dict_coreset_size(spark):
    """
    pass coreset size as dict (number of samples for each class)
    """
    df, _ = create_large_simple_data_rdd(spark=spark, base_number=210, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    chunk_size = 20

    print(chunk_size)

    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN
    coreset_size_dict = {0: 5, 1: 10}
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=coreset_size_dict,
        chunk_sample_ratio=0.0,
        data_params=data_params,
        dhspark_path=test_output_folder)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=test_output_folder)
    for level in tree.tree_ldf:
        grouped = level.level_df.toPandas().groupby(['y', 'chunk_index']).size().reset_index(name='count')
        assert grouped[grouped['y'] == 0]['count'].max() <= coreset_size_dict[0]
        if not np.isnan(grouped[grouped['y'] == 1]['count'].max()):
            assert grouped[grouped['y'] == 1]['count'].max() <= coreset_size_dict[1]


def test_dict_build_params(spark):
    """
    Test  build with coreset param change: fair,deterministic_size,det_weights_behaviour
    """

    df, _ = create_large_simple_data_rdd(spark=spark, base_number=210, column_numbers=5, target_column_name="y",
                                         target_column_number=0, power_number=1)
    chunk_size = 20

    print(chunk_size)

    delete_all_files(test_output_folder)
    data_params = DATA_PARAMS_PLAIN

    coreset_params = {
        'fair': 'fair',
        'deterministic_size': .777,
        'det_weights_behaviour': 'det_weights_behaviour',
    }

    class_size_values = {0: 10, 1: 10}
    smple_all_value = ["f1"]
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2,
        chunk_sample_ratio=0.0,
        data_params=data_params,
        dhspark_path=test_output_folder, class_size=class_size_values, coreset_params=coreset_params,
        sample_all=smple_all_value)
    service.build_preprocess_from_df(input_df=df, spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=test_output_folder)
    service._init_coreset()
    coreset = service._tree_params.coreset
    assert coreset._det_weights_behaviour == coreset_params["det_weights_behaviour"]
    assert coreset._deterministic_size == coreset_params["deterministic_size"]

    ## since i dont have access to the coreset i have tried to mniplate and use privat functions
    def dummy_build(
            X, y, coreset_size, new_state, w,
            class_size=None, sample_all=None):
        assert class_size == class_size_values
        assert sample_all == smple_all_value

        coreset.sensitivities = np.ones(X.shape[0])
        return np.arange(X.shape[0]), np.ones(X.shape[0])

    coreset.build = dummy_build

    pdf = service._udf_create_coreset(key=1, pdf=tree.getChunkDataNoCoresetDF().toPandas(), coreset=coreset,
                                      coreset_size=service._tree_params.coreset_size,
                                      sample_all=service._tree_params.sample_all,
                                      class_size=service._tree_params.class_size,
                                      target_column=service._tree_params.target_column)

    service.build(spark_session=spark)
