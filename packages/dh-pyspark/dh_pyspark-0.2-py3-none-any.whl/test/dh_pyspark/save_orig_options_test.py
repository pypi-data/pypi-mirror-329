import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import pytest
from pyspark.ml.linalg import SparseVector, DenseVector

from dh_pyspark.model.tree_model import SaveOrig
from dh_pyspark.services._coreset_service_base import OutputFormat, PreprocessingStage
from dh_pyspark.services.coreset.dtc import CoresetTreeServiceDTC
from test.dh_pyspark.utils import delete_all_files, get_dataset

test_output_folder = "test_output"


@pytest.mark.parametrize('dataset_numeric_only', [False, True])
@pytest.mark.parametrize('save_orig', [
    SaveOrig.PREPROCESSING_ONLY,
    SaveOrig.NONE,
    SaveOrig.PREPROCESSING_AND_BUILD
])
@pytest.mark.parametrize('output_format', [
    OutputFormat.SPARK_DF,
    OutputFormat.MATRIX,
    OutputFormat.PANDAS_DF,
])
@pytest.mark.parametrize('return_sparse', [False, True])
@pytest.mark.parametrize('preprocessing_stage', [
   PreprocessingStage.USER_NO_MISSING_VALUES,
   PreprocessingStage.AUTO,
   PreprocessingStage.USER,
])
def test_get_coreset_combinations(
        spark,
        dataset_numeric_only,
        save_orig,
        output_format,
        return_sparse,
        preprocessing_stage
):
    dataset_has_missing_values = True
    delete_all_files(test_output_folder)
    chunk_size = 20
    chunk_sample_ratio = 0.8
    coreset_size = 0.8
    df, data_params = get_dataset(spark, numeric_only=dataset_numeric_only, missing_values=dataset_has_missing_values)
    service = CoresetTreeServiceDTC(chunk_size=chunk_size, coreset_size=coreset_size,
                                    chunk_sample_ratio=chunk_sample_ratio,
                                    data_params=data_params,
                                    dhspark_path=test_output_folder,
                                    save_orig=save_orig
                                    )
    service.build_preprocess_from_df(spark_session=spark, input_df=df)
    service.build(spark_session=spark)

    sparse_threshold = 2 if return_sparse else 0
    if (save_orig == SaveOrig.NONE
            and not (dataset_numeric_only and preprocessing_stage == PreprocessingStage.USER_NO_MISSING_VALUES)):
        try:
            service.get_coreset(
                spark_session=spark,
                preprocessing_stage=preprocessing_stage,
                sparse_threshold=sparse_threshold,
                output_format=output_format
            )
        except RuntimeError as error:
            error_text = error.args[0]
            assert error_text == ('In order to get original data one '
                                  'should set parameter save_orig = True on '
                                  'the service object initialization')
    else:
        feature_names = [col.name for col in data_params.features]
        num_feature_names = [col.name for col in data_params.features if not col.categorical]
        coreset = service.get_coreset(
            spark_session=spark,
            preprocessing_stage=preprocessing_stage,
            sparse_threshold=sparse_threshold,
            output_format=output_format
        )
        if preprocessing_stage == PreprocessingStage.AUTO:
            if output_format == OutputFormat.SPARK_DF:
                assert "features" in coreset.columns
                one_feature_value = coreset.collect()[0].features
                assert isinstance(one_feature_value, SparseVector if return_sparse else DenseVector)
                assert (len(DenseVector(one_feature_value)) == sum(service._get_categories_lengths()) +
                        len(service._tree_params.numeric_columns))
                for feature in feature_names:
                    assert feature not in coreset.columns
            elif output_format == OutputFormat.PANDAS_DF:
                assert isinstance(coreset['X'], pd.DataFrame)
                for num_col in num_feature_names:
                    num_col in coreset['X'].columns
                # TODO provide something like this -
                # TODO assert X.shape[1] == sum(service._get_categories_lengths()) + len(num_feature_names)
            elif output_format == OutputFormat.MATRIX:
                type_of_data = csr_matrix if return_sparse else np.ndarray
                assert isinstance(coreset['X'], type_of_data)
                assert len(coreset['y']) == len(coreset['w'])
                X = coreset['X'].toarray() if return_sparse else coreset['X']
                assert len(coreset['y']) == X.shape[0]
                assert X.shape[1] == sum(service._get_categories_lengths()) + len(num_feature_names)
        else:
            if output_format == OutputFormat.SPARK_DF:
                assert "features" not in coreset.columns
                for feature in feature_names:
                    assert feature in coreset.columns
            elif output_format == OutputFormat.PANDAS_DF:
                assert isinstance(coreset['X'], pd.DataFrame)
                for num_col in num_feature_names:
                    num_col in coreset['X'].columns
                # TODO provide something like this -
                # TODO assert X.shape[1] == sum(service._get_categories_lengths()) + len(num_feature_names)
            elif output_format == OutputFormat.MATRIX:
                assert isinstance(coreset['X'], np.ndarray)
                assert len(coreset['y']) == len(coreset['w'])
                X = coreset['X']
                assert len(coreset['y']) == X.shape[0]
                assert X.shape[1] == len(feature_names)
                if dataset_numeric_only:
                    assert isinstance(coreset['X'][0][-1], np.number)
                else:
                    if X[0][-1] is not None:
                        assert isinstance(X[0][-1], str)
