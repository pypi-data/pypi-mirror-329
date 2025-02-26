import pandas as pd
import pytest
from pyspark.ml.linalg import SparseVector, DenseVector
from scipy.sparse import csr_matrix

from dh_pyspark.services._coreset_service_base import OutputFormat
from dh_pyspark.services.coreset.dtc import CoresetTreeServiceDTC
from test.dh_pyspark.utils import delete_all_files, get_dataset
import numpy as np

test_output_folder = "test_output"


@pytest.mark.parametrize('output_format', [
    OutputFormat.SPARK_DF,
    OutputFormat.MATRIX,
    OutputFormat.PANDAS_DF,
])
@pytest.mark.parametrize('return_sparse', [False, True])
def test_auto_preprocessing(spark, output_format, return_sparse):
    sparse_threshold = 2 if return_sparse else 0
    delete_all_files(test_output_folder)
    chunk_size = 20
    chunk_sample_ratio = 0.8
    coreset_size = 0.8
    df, data_params = get_dataset(spark, numeric_only=False, missing_values=True)
    service = CoresetTreeServiceDTC(
        chunk_size=chunk_size,
        coreset_size=coreset_size,
        chunk_sample_ratio=chunk_sample_ratio,
        data_params=data_params,
        dhspark_path=test_output_folder
    )
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)
    df_out = service.auto_preprocessing(
        spark_session=spark,
        df=df,
        output_format=output_format,
        sparse_threshold=sparse_threshold
    )
    num_of_output_features = 11

    if output_format == OutputFormat.SPARK_DF:
        assert set(df_out.columns) == set([service._tree_params.target_column, 'features'])
        assert isinstance(df_out.toPandas()['features'][0], SparseVector if return_sparse else DenseVector)
        y = df_out.toPandas()[service._tree_params.target_column].to_numpy()
        assert len(df_out.toPandas()['features'][0]) == num_of_output_features
        assert df_out.count() == df.count()
    elif output_format == OutputFormat.PANDAS_DF:
        assert isinstance(df_out['X'], pd.DataFrame)
        y = df_out['y']
        dense_X = df_out['X'].to_numpy()
        assert dense_X.shape == (df.count(), num_of_output_features)
    else:
        if return_sparse:
            assert isinstance(df_out['X'], csr_matrix)
            dense_X = df_out['X'].toarray()
            assert dense_X.shape == (df.count(), num_of_output_features)
        else:
            assert isinstance(df_out['X'], np.ndarray)
            dense_X = df_out['X']
            assert dense_X.shape == (df.count(), num_of_output_features)
        y = df_out['y']

    # check if target is indexed
    assert set(np.unique(y)) == set([1, 2])




