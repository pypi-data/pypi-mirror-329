from dataheroes.data.common import DataParams
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier

from dh_pyspark.common.utills import create_large_simple_data_rdd, create_random_dataframe_start_end_date
from dh_pyspark.services.coreset.dtc import CoresetTreeServiceDTC
from test.dh_pyspark.get_coreset_test import test_output_folder
from test.dh_pyspark.utils import check_tree, delete_all_files


def test_fit_coreset(spark):
    features_number = 4
    df, _ = create_large_simple_data_rdd(
        spark=spark,
        base_number=100,
        column_numbers=features_number + 1,
        target_column_name="y",
        target_column_number=0
    )
    print(f'{df.count()=}')
    chunk_size = df.count() // 64

    tree_data_path = test_output_folder

    delete_all_files(tree_data_path)
    features = ({"name": f"f{i}"} for i in range(1, features_number + 1))
    target = 'y'
    data_params_dic = {
        'features': features,
        'target': {'name': target},
    }
    data_params = DataParams.from_dict(data_params_dic)
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=0.2, chunk_sample_ratio=0.4,
                                    data_params=data_params,
                                    dhspark_path=tree_data_path)
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    tree = service._load(spark=spark, dhspark_path=tree_data_path)
    check_tree(coreset_tree=tree, df=df, chunk_size=chunk_size)
    model = service.fit(spark_session=spark, transformer_cls=LogisticRegression, level=3)
    assert model is not None
    coreset_df = service.get_coreset(spark_session=spark, level=5)
    coreset_df.show()
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0
    model = service.fit(spark_session=spark, transformer_cls=RandomForestClassifier, level=3)
    assert model is not None
    coreset_df = service.get_coreset(spark_session=spark, level=5)
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0
    model = service.fit(spark_session=spark, transformer_cls=GBTClassifier, level=3)
    assert model is not None
    coreset_df = service.get_coreset(spark_session=spark, level=5)
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0
    model = service.fit(spark_session=spark, transformer_cls=LogisticRegression, level=2, regParam=0.1,
                        elasticNetParam=1.0, family="multinomial")
    assert model is not None
    assert model.coefficientMatrix is not None
    assert model.coefficientMatrix is not None
    coreset_df = service.get_coreset(spark_session=spark, level=5)
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0


def test_fit_seq_coreset(spark):
    row_number = 60
    chunk_size = None
    date_format = '%Y-%m-%d'
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

    df = create_random_dataframe_start_end_date(spark=spark, start_date='2024-04-01',
                                                end_date='2024-04-30', num_columns=5, num_rows=row_number,
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

    model = service.fit(spark_session=spark, transformer_cls=LogisticRegression, seq_from="2024-04-01",
                        seq_to="2024-04-10")
    coreset_df = service.get_coreset(spark_session=spark, seq_from="2024-04-01", seq_to="2024-04-10")
    assert model is not None
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0
    model = service.fit(spark_session=spark, transformer_cls=RandomForestClassifier, seq_from="2024-04-01",
                        seq_to="2024-04-10")
    assert model is not None
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0
    model = service.fit(spark_session=spark, transformer_cls=GBTClassifier, seq_from="2024-04-01",
                        seq_to="2024-04-10")
    assert model is not None
    predict_df = model.transform(coreset_df)
    assert predict_df.count() > 0
