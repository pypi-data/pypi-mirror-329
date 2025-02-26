import numpy as np
from dataheroes.data.common import DataParams

from dh_pyspark.common.utills import create_large_simple_data_rdd, create_random_dataframe_start_end_date
from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services._coreset_service_base import CoresetTreeServiceBase, DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES
from dh_pyspark.services.coreset.dtc import CoresetTreeServiceDTC
from test.dh_pyspark.utils import delete_all_files, print_tree

test_output_folder = "test_output"


def test_orphans():
    service = CoresetTreeServiceDTC(dhspark_path=test_output_folder)
    orphans = service._get_orphan_for_level(10, 2, 7)
    assert orphans == [(0, 9), (0, 10), (0, 11)]


def test_get_coreset_tree(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[0])
    chunk_size, df, features_number = create_df_and_chunk(spark, number_of_chunks=64)
    tree_data_path = test_output_folder
    delete_all_files(tree_data_path)
    features = ({"name": f"f{i}"} for i in range(1, features_number + 1))
    target = 'y'
    data_params_dic = {
        'features': features,
        'target': {'name': target},
    }
    data_params = DataParams.from_dict(data_params_dic)
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size,
        coreset_size=0.2,
        chunk_sample_ratio=0.2,
        data_params=data_params,
        dhspark_path=tree_data_path,
    )
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)

    coreset_size = chunk_size * 0.2
    for level in range(3):
        df_coreset = service.get_coreset(spark_session=spark, level=level)
        # transform to numpy arrays
        x = np.array([row["features"].toArray() for row in df_coreset.collect()])
        y = df_coreset.select([target]).toPandas().to_numpy().flatten()
        w = df_coreset.select(['w']).toPandas().to_numpy().flatten()

        # check sizes of arrays
        num_of_samples = int((2 ** level) * coreset_size)
        num_of_samples_min = int(num_of_samples * 0.4)
        num_of_samples_max = int(num_of_samples * 2)
        print(f'{level=} {x.shape=} {num_of_samples_min=} {num_of_samples_max=}')
        assert x.shape[1] == features_number
        assert (x.shape[0] > num_of_samples_min) and (x.shape[0] < num_of_samples_max)
        assert len(w) == x.shape[0]
        assert len(y) == x.shape[0]


def create_df_and_chunk(spark, number_of_chunks):
    features_number = 4
    df, _ = create_large_simple_data_rdd(
        spark=spark,
        base_number=100,
        column_numbers=features_number + 1,
        target_column_name="y",
        target_column_number=0
    )
    print(f'{df.count()=}')
    chunk_size = df.count() // number_of_chunks
    return chunk_size, df, features_number


def test_get_coreset_for_seq(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[0])
    row_number = 211
    chunk_size = 7
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

    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    chunk_sample_ratio = 0.6
    coreset_size = 0.2
    chunk_by = "date"

    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, chunk_sample_ratio=chunk_sample_ratio, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    print_tree(coreset_tree, 200)
    pd_df = service._find_closest_match_chunks(service._tree_params.chunk_by_tree, seq_from='2024-04-05 00:00:00',
                                               seq_to='2024-04-15 00:00:00')
    print(pd_df)
    coreset_df = service.get_coreset(spark_session=spark, seq_from='2024-04-05 00:00:00', seq_to='2024-04-15 00:00:00')
    assert coreset_df.count() > 0
    # in enhance mode the date column is not formatted and remain string
    assert coreset_df.dtypes[0][1] == 'string'
    coreset_df.show(truncate=False)
    assert coreset_df.select("chunk_index", "level").dropDuplicates().count() == len(pd_df)


def test_get_coreset_level0_chunk_date(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, 'false')
    row_number = 211
    chunk_size = 5
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
    print_tree(coreset_tree, 200, column_list=["date", "level", "chunk_index"])
    print("metadata tree")
    print(service._tree_params.chunk_by_tree)
    coreset_df = service.get_coreset(spark_session=spark, seq_from="2024-04-08 00:00:00", seq_to="2024-04-08 00:00:00")
    coreset_df.show(n=200)
    assert coreset_df.count() > 0
    assert coreset_df.dtypes[0][1] == 'date'


def test_get_coreset_for_seq_root(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[0])
    row_number = 60
    chunk_size = None
    date_format = '%Y-%m-%d %H:%M:%S'
    data_params = {
        'features': list(({"name": f"f{i}"} for i in range(2, 4))),
        'target': {'name': 'y'},
        'fill_value_num': 0,
        'seq_column':
            {
                'name': 'date',
                'granularity': 'D',
                'datetime_format': date_format,
                'chunk_by': True
            },
    }

    df = create_random_dataframe_start_end_date(spark=spark, start_date='2024-04-01 08:00:00',
                                                end_date='2024-04-04 08:00:00', num_columns=5, num_rows=row_number,
                                                date_format=date_format, granularity="D")
    indexer_meth_data_path = test_output_folder
    delete_all_files(indexer_meth_data_path)
    chunk_sample_ratio = 0.6
    coreset_size = 0.2
    chunk_by = "date"

    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, chunk_sample_ratio=chunk_sample_ratio, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    print_tree(coreset_tree, 200)
    print(service._tree_params.chunk_by_tree)
    pd_df = service._find_closest_match_chunks(service._tree_params.chunk_by_tree, seq_from='2024-04-01 08:00:00',
                                               seq_to='2024-04-04 08:00:00')
    print(pd_df)
    coreset_df = service.get_coreset(spark_session=spark, seq_from='2024-04-01 08:00:00', seq_to='2024-04-04 08:00:00')
    assert coreset_df.count() > 0

    coreset_df.show(truncate=False)
    assert coreset_df.select("chunk_index", "level").dropDuplicates().count() == len(pd_df)
    assert coreset_df.select("chunk_index", "level").dropDuplicates().count() == 1
    collect = coreset_df.select("level", "chunk_index").distinct().collect()
    assert collect[0][0] == coreset_tree.getTreeSize() - 1
    assert collect[0][1] == 1


def test_get_coreset_for_seq_hourly(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[0])
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
    chunk_sample_ratio = 0.6
    coreset_size = 0.2
    chunk_by = "date"

    service = CoresetTreeServiceDTC(
        coreset_size=coreset_size, chunk_sample_ratio=chunk_sample_ratio, data_params=data_params,
        dhspark_path=indexer_meth_data_path, chunk_by=chunk_by, chunk_size=chunk_size)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_tree = service._load(spark=spark, dhspark_path=indexer_meth_data_path)
    print_tree(coreset_tree=coreset_tree, number_rows=row_number)
    pd_df = service._find_closest_match_chunks(service._tree_params.chunk_by_tree, seq_from='2024-04-02 08:30:00',
                                               seq_to='2024-04-02 23:30:00')
    print(pd_df)
    coreset_df = service.get_coreset(spark_session=spark, seq_from='2024-04-02 08:30:00', seq_to='2024-04-02 23:30:00')
    assert coreset_df.count() > 0
    coreset_df.show(truncate=False)
    assert coreset_df.select("chunk_index", "level").dropDuplicates().count() == len(pd_df)


def test_get_coreset_split_columns(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, 'false')
    df, features_number, target = get_coreset_data(spark, "user")
    assert df.count() > 0
    assert set(df.columns) == set([f"f{i}" for i in range(1, features_number + 1)] +
                                  ['w', target])


def get_coreset_data(spark, preprocess):
    chunk_size, df, features_number = create_df_and_chunk(spark, number_of_chunks=64)
    tree_data_path = test_output_folder
    delete_all_files(tree_data_path)
    features = ({"name": f"f{i}"} for i in range(1, features_number + 1))
    target = 'y'
    data_params_dic = {
        'features': features,
        'target': {'name': target},
    }
    data_params = DataParams.from_dict(data_params_dic)
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size, coreset_size=0.2,
        chunk_sample_ratio=0.2, data_params=data_params, dhspark_path=tree_data_path,
        save_orig=SaveOrig.PREPROCESSING_ONLY
    )
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    coreset_output_path = f"{tree_data_path}/get_coreset"
    service.get_coreset(spark_session=spark, level=4, save_path=coreset_output_path, preprocessing_stage=preprocess)
    df = spark.read.parquet(coreset_output_path)
    return df, features_number, target


def test_get_coreset_split_trace_mode_columns(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[0])
    df, features_number, target = get_coreset_data(spark, "user")
    f_columns = ([f"f{i}" for i in range(1, features_number + 1)] +
                 ["level", "row_index_id", "chunk_index", "sensitivity", "w", target])
    assert df.count() > 0
    assert set(f_columns) == set(df.columns)


def test_get_coreset_auto_trace_mode_columns(spark):
    spark.conf.set(DHSPARK_TRACE_MODE_CONF, TRACE_MODE_VALUES[1])
    df, features_number, target = get_coreset_data(spark, "auto")
    assert df.count() > 0
    assert set([target, "features", "level", "row_index_id", "chunk_index", "sensitivity", "w"]) == set(
        df.columns)


def test_coreset_on_chunk_by_tree():
    date_format = '%Y-%m-%d %H:%M:%S'
    data_params = {
        'features': list(({"name": f"f{i}"} for i in range(2, 500))),
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
    service = CoresetTreeServiceBase(dhspark_path="", data_params=data_params)
    with open('chunk_by_tree_data/10b_2m_chunk_by_tree.json', 'r') as file:
        str_data = file.read()
        chunk_by_tree = service._chunk_tree_from_json(str_data)
        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-06-14",
                                                          seq_to="2023-06-16")
        print(match_chunks)
        assert len(match_chunks) == 2
        chunk_by_tree = service._chunk_tree_from_json(str_data)
        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-06-13",
                                                          seq_to="2023-06-17")
        print(match_chunks)
        assert len(match_chunks) == 8
        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-06-10",
                                                          seq_to="2023-06-12")
        print(match_chunks)
        assert len(match_chunks) == 4
        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-06-13",
                                                          seq_to="2023-06-16")
        print(match_chunks)
        assert len(match_chunks) == 6
        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-12-29",
                                                          seq_to="2023-12-31")
        print(match_chunks)
        assert len(match_chunks) == 1
        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-12-17",
                                                          seq_to="2023-12-19")
        print(match_chunks)
        assert len(match_chunks) == 5

        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-11-28",
                                                          seq_to="2023-11-30")
        print(match_chunks)
        assert len(match_chunks) == 3

        match_chunks = service._find_closest_match_chunks(tree_metadata=chunk_by_tree, seq_from="2023-10-01",
                                                          seq_to="2023-12-31")
        print(match_chunks)
        assert len(match_chunks) == 35
