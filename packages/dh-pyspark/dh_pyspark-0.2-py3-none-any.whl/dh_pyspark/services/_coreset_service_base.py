import json
import logging
import os
from builtins import list
from datetime import datetime, timedelta
from typing import Union

import numpy as np
import pandas as pd
import pyspark.ml.functions as mf
import pyspark.sql.functions as f
import pyspark.sql.functions as sqlf
import scipy.sparse as scipy_sparse
from dataheroes.core.coreset._base import CoresetBase
from dataheroes.data.common import DataParams, FeatureField
from dataheroes.services.common import CoresetParams
from pyspark.ml import Pipeline
from pyspark.ml.feature import Imputer
from pyspark.ml.linalg import SparseVector, VectorUDT, DenseVector
from pyspark.ml.feature import Imputer, VectorAssembler, OneHotEncoder
from pyspark.sql import DataFrame, Window
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, DoubleType, StructType, IntegerType, StringType, ArrayType, MapType, \
    BooleanType
from scipy.sparse import csr_matrix

from dh_pyspark.common.utills import convert_pandas_date_format_to_spark_date_format
from dh_pyspark.common.utills import set_udf_logging, get_fully_qualified_name, get_class_from_fully_qualified_name
from dh_pyspark.model.tree_model import SaveOrig, TreeDataFrame, LevelDataFrame, TreeParams
from dh_pyspark.transformer.transformers import PersistStringIndexer

MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE = 0.6
SUB_CHUNK_PREFIX = "_sc_"
DHSPARK_TRACE_MODE_CONF = "spark.dhspark.traceMode"
# enhanced can be run on a cluster enhance_local_only can not be run in a cluster only for tests
TRACE_MODE_VALUES = ["enhanced",
                     "enhanced_local_only"]


class OutputFormat:
    SPARK_DF = 'spark_df'
    PANDAS_DF = 'pandas_df'
    MATRIX = 'matrix'


def _get_matrix(numerical_data, one_hot_indices, cat_lengths):
    category_offsets = np.cumsum([0] + cat_lengths)
    row_indices = []
    col_indices = []
    for row_idx, indices in enumerate(one_hot_indices):
        for col_idx, cat_index in enumerate(indices):
            absolute_index = category_offsets[col_idx] + int(cat_index)
            row_indices.append(row_idx)
            col_indices.append(absolute_index)
    one_hot_data = np.ones(len(row_indices))
    total_one_hot_dim = category_offsets[-1]
    one_hot_matrix = csr_matrix(
        arg1=(one_hot_data, (row_indices, col_indices)),
        shape=(numerical_data.shape[0], total_one_hot_dim)
    )
    matrix = scipy_sparse.hstack([csr_matrix(numerical_data), one_hot_matrix])
    return matrix


class PreprocessingStage:
    USER_NO_MISSING_VALUES = 'user_no_missing_vals'
    USER = 'user'
    AUTO = 'auto'


class CoresetTreeServiceBase:
    coreset_cls = CoresetBase
    coreset_params_cls = CoresetParams

    def __init__(self, *, dhspark_path, data_params: Union[DataParams, dict] = None,
                 chunk_size: int = None, n_instances: int = None, n_instances_exact: bool = None,
                 chunk_by=None, coreset_size=None, coreset_params: Union[CoresetParams, dict] = None,
                 sample_all=None, chunk_sample_ratio=None, class_size=None,
                 save_orig: SaveOrig = SaveOrig.NONE
                 ):
        """
                initializing class with data for tree construction. this function prepare and go over the input data
                adding index and chunk id creating feature array and ohe the categorical data.
                and create the data for validation

                Parameters:
                    chunk_size (float): int, optional.
                    The number of instances to be used when creating a coreset node in the tree.
                    chunk_size=0: Nodes are created based on input chunks.
                    chunk_size=-1: Force the service to create a single coreset
                    from the entire dataset (if it fits into memory).	None
                    coreset_size: Coreset size could be either int or to receive the proportion of the classes,
                     e.g. {0: 950K, 1: 50K}, or we pass coreset_size=0.2 and class_proportions={0: 0.95, 1: 0.05}.
                    chunk_sample_ratio (float): Validation row factor.
                    n_instances: Number of instances of the new data.
                    n_instances_exact (bool): if true we will use n_instances param in calculating max chunk
                    and save time should be used only when the user knows the exact number of data instances.
                    data_params (DataParams): Data parameters.
                    dhspark_path (str): Path to metadata where to save the tree and data of the coreset tree.
                    chunk_by (str): Column Optional Split the data according to the provided column.
                    When provided, chunk_size input is ignored.
                    class_size: Classification only. Number of data instances to sample per class.
                     Classes already in `sample_all` are ignored.
                    sample_all: Classification only. Classes in this list will have all samples returned.
                    save_orig: The different values reflect ways of the original data handling.<br/><br/>
                        - **SaveOrig.NONE** - Do not save original data (default).<br/><br/>
                        - **SaveOrig.PREPROCESSING_ONLY** - Save original data, in order to make possible to get
                        original data by `get_coreset` method, passing parameter preprocessing_stage = 'user'`.<br/><br/>
                        - **SaveOrig.PREPROCESSING_AND_BUILD** - Save original data, in order to make possible to get
                        original data by `get_coreset` method, passing parameter `preprocessing_stage = 'user'`.
                        This option should be used when it's necessary to make `get_coreset` faster.  Build for this
                        case should be slightly slower than for `SaveOrig.PREPROCESSING_AND_BUILD`.<br/><br/>
                """
        coreset_params_val = coreset_params or self.coreset_params_cls()
        if isinstance(coreset_params_val, dict):
            coreset_params_val = self.coreset_params_cls(**coreset_params_val)
        data_params_val = data_params
        if isinstance(data_params, dict):
            data_params_val = DataParams.from_dict(data_params)

        # adding this to align with the library coreset size calculation
        if coreset_size is not None and isinstance(coreset_size, (float, np.floating)):
            coreset_size = min(coreset_size, MAX_RATIO_CORESET_SIZE_TO_CHUNK_SIZE)
        self._tree_params = TreeParams(dhspark_path=dhspark_path,
                                       chunk_size=chunk_size,
                                       coreset_size=coreset_size,
                                       chunk_sample_ratio=chunk_sample_ratio,
                                       n_instances=n_instances, n_instances_exact=n_instances_exact,
                                       data_params=data_params_val,
                                       chunk_by=chunk_by,
                                       class_size=class_size,
                                       sample_all=sample_all,
                                       coreset_params=coreset_params_val,
                                       save_orig=save_orig)

    def _build_preprocess(self, spark_session: SparkSession, input_df: DataFrame = None):
        """
        Create and build data for tree construction. this function prepare and go over the input data
        adding index and chunk id creating feature array and ohe the categorical data.
        and create the data for validation


        Parameters:
            spark_session (SparkSession): the SparkSession object.
            input_df (DataFrame): New input data frame.

        """
        source_df = input_df

        spark_session.sparkContext.setJobDescription("Starting build_preprocess Task")

        # Create TreeDataFrame object for coreset tree
        coreset_tree = TreeDataFrame()
        self._tree_params.categorical_columns = [col.name for col in self._tree_params.data_params.features
                                                 if col.categorical]
        self._tree_params.numeric_columns = [col.name for col in self._tree_params.data_params.features
                                             if not col.categorical]
        tree_params = self._tree_params
        self._set_chunk_sample_ratio()

        level = 0
        self._set_trace_mode(spark_session=spark_session)
        # Select relevant columns from source DataFrame
        spark_session.sparkContext.setJobDescription("build_preprocess - Select data Columns")
        data_column_list, target_name, index_name, df = self._select_columns(chunk_by=tree_params.chunk_by,
                                                                             data_params=tree_params.data_params,
                                                                             df=source_df)
        tree_params.index_column = index_name
        # Handle missing values in DataFrame
        spark_session.sparkContext.setJobDescription("build_preprocess - Handle Missing values")
        df = self._handle_missing_values_params(df)

        # Create index and chunk the data
        spark_session.sparkContext.setJobDescription("build_preprocess - Create index and chunk index")
        df, calc_column_names = self._create_index_and_chunk(
            chunk_size=tree_params.chunk_size, level=level, df=df,
            chunk_by=tree_params.chunk_by, index_column=tree_params.index_column)

        # Calculate maximum chunk index
        spark_session.sparkContext.setJobDescription("build_preprocess - get Max chunk index")
        max_chunk = self._calculate_max_chunk_index(df=df, chunk_by=tree_params.chunk_by)
        tree_params.first_level_max_chunk = max_chunk

        # Perform data preprocessing transformations
        spark_session.sparkContext.setJobDescription("build_preprocess - Preprocess Transformers - String Indexer")
        df, _, target_name, transform_added_columns = self._data_preprocess_transformers(
            df=df,
            spark=spark_session,
            target_column=tree_params.data_params.target.name,
            dhspark_path=tree_params.dhspark_path,
            data_params=tree_params.data_params
        )
        tree_params.target_column = target_name

        calc_column_names = calc_column_names + transform_added_columns
        calc_column_names.append(target_name)
        tree_params.calc_column_names = calc_column_names
        df = df.select(calc_column_names)
        # Set DataFrame for chunk date without coreset
        self._handle_data_no_coreset(df=df, coreset_tree=coreset_tree)
        self._save_create_data(coreset_tree=coreset_tree, spark=spark_session)

        # Handle validation data
        spark_session.sparkContext.setJobDescription("build_preprocess - Create Validation Data")
        coreset_tree = self._handle_validation_data(coreset_tree=coreset_tree)

        # Save data before tree construction
        spark_session.sparkContext.setJobDescription("build_preprocess - Save Data")
        self._save_validation_and_metadata_for_build(coreset_tree=coreset_tree, spark=spark_session)

    def build_preprocess_from_df(self, spark_session: SparkSession, input_df: DataFrame):
        """
        Create and build data  from input data frame for tree construction.
        this function prepare and go over the input data adding index and chunk id creating feature array and ohe
        the categorical data. and create the data for validation


        Parameters:
            spark_session (SparkSession): the SparkSession object.
            input_df (DataFrame): source input data frame the data to build the coreset tree from.

        """
        self._build_preprocess(spark_session=spark_session, input_df=input_df)

    def build_preprocess_from_file(self, spark_session: SparkSession, input_path: str, input_format: str = "parquet"):
        """
        Create and build data  from input files or directory of parquet files for tree construction.
        this function prepare and go over the input data
        adding index and chunk id creating feature array and ohe the categorical data.
        and create the data for validation


        Parameters:
            spark_session (SparkSession): the SparkSession object.
            input_path (DataFrame): source input files in parquet format the data to build the coreset tree from.
            input_format (str) the type of input file/s to read parquet is default csv or json.


        """

        source_df = spark_session.read.format(input_format).option("header", "true").option("inferSchema", "true").load(
            input_path)
        self._build_preprocess(spark_session=spark_session, input_df=source_df)

    def _build(self, spark_session: SparkSession, stop_level: int = None):
        """
        Build a tree using the provided coreset and metadata. befre calling this function you mast call build_preprocess

        Parameters:
            spark_session (SparkSession): the SparkSession object.
            stop_level (int) : the level to stop building the tree since the first level needs more cloud resources
            usually we have a step crating the first level (level 0) only and then a step crating the rest of the tree

        Returns:
            None
        """
        level = 0

        # Load the tree from metadata
        coreset_tree = self._load(spark=spark_session, dhspark_path=self._tree_params.dhspark_path)
        tree_params = self._tree_params
        self._init_coreset()
        # tree_params.coreset._det_weights_behaviour = self._tree_params.det_weights_behaviour
        # support for stop level to build each level at a different session
        tree_params.stop_level = stop_level
        max_chunk = tree_params.first_level_max_chunk
        if tree_params.stop_level_max_chunk is not None:
            max_chunk = tree_params.stop_level_max_chunk

        # Calculate coreset tree
        spark_session.sparkContext.setJobDescription("build - Create Tree")
        self._calculate_coreset(coreset_tree=coreset_tree, level=level, max_chunk=max_chunk,
                                coreset=tree_params.coreset,
                                spark=spark_session,
                                target_column=tree_params.target_column)

        # Save tree metadata
        spark_session.sparkContext.setJobDescription("build - Save Meta Data")
        self._save_metadata(coreset_tree=coreset_tree, spark=spark_session)

        print("Finish Saving tree")

    def build(self, spark_session: SparkSession, stop_level: int = None):
        """
        Build a tree using the provided coreset and metadata. before calling this function you mast call
        build_preprocess_from_file/df

        Parameters:
            spark_session (SparkSession): the SparkSession object.
            stop_level (int) : the level to stop building the tree since the first level needs more cloud resources
            usually we have a step crating the first level (level 0) only and then a step crating the rest of the tree

        Returns:
            None
        """
        self._build(spark_session=spark_session, stop_level=stop_level)

    def _partial_build_preprocess(self, spark_session: SparkSession, input_df: DataFrame = None):
        """
        Creates partial build for an existing coreset tree and adding new data.

        Args:
        - spark_session: SparkSession object.
        - input_df: DataFrame containing new data to add to the tree.
        Returns:
        None
        """

        spark_session.sparkContext.setJobDescription("Starting partial_build_preprocess Task")

        # Load source DataFrame if provided
        source_df = input_df

        # Load coreset tree metadata
        coreset_tree = self._load(spark_session, self._tree_params.dhspark_path)
        tree_params = self._tree_params
        self._set_chunk_sample_ratio()

        level = 0

        # Select relevant columns from source DataFrame
        data_column_list, target_name, index_name, df = self._select_columns(chunk_by=self._tree_params.chunk_by,
                                                                             data_params=self._tree_params.data_params,
                                                                             df=source_df)

        spark_session.sparkContext.setJobDescription("partial_build_preprocess - Handling Missing values")

        # Handle missing values in DataFrame
        df = self._handle_missing_values_params(df)

        spark_session.sparkContext.setJobDescription(
            "partial_build_preprocess - Calculate Starting Chunk Index Row Index")
        # Calculate starting chunk index and row index from the row no corest data to get a continus index
        starting_index = None
        ending_chunk_by = None
        if tree_params.chunk_by is None:
            max_value = \
                coreset_tree.getChunkDataNoCoresetDF().where(f.col("chunk_index") == tree_params.first_level_max_chunk) \
                    .agg(f.max(f"row_index_id").alias("max_row_index_id")).collect()[0].asDict()
            starting_index = max_value["max_row_index_id"] + 1
        else:
            max_value = \
                coreset_tree.getChunkDataNoCoresetDF().where(f.col("chunk_index") == tree_params.first_level_max_chunk) \
                    .agg(f.max(tree_params.chunk_by).alias("max_chunk_by")).collect()[0].asDict()
            ending_chunk_by = max_value["max_chunk_by"]

        old_max_chunk = tree_params.first_level_max_chunk
        starting_chunk = old_max_chunk + 1
        tree_params.partial_build_starting_index = starting_index
        tree_params.partial_build_ending_chunk_by = ending_chunk_by

        spark_session.sparkContext.setJobDescription("partial_build_preprocess - Create index and chunk")

        # Create index and chunk for partial build
        df, calc_column_names = self._create_index_and_chunk(chunk_size=tree_params.chunk_size, level=level,
                                                             index_start=starting_index,
                                                             chunk_start=starting_chunk,
                                                             df=df,
                                                             chunk_by=tree_params.chunk_by,
                                                             index_column=tree_params.index_column)

        spark_session.sparkContext.setJobDescription("partial_build_preprocess - get Max chunk index")
        # Calculate new max chunk index
        max_chunk = self._calculate_max_chunk_index(df=df, chunk_by=tree_params.chunk_by,
                                                    last_max_chunk=tree_params.first_level_max_chunk)
        tree_params.first_level_max_chunk = max_chunk
        tree_params.first_level_last_max_chunk = old_max_chunk

        spark_session.sparkContext.setJobDescription("partial_build_preprocess - Categorical and data Transformation")
        # Handle data preprocessing and transformation
        df, diff_map, target_name, transform_added_columns = self._data_preprocess_transformers(
            df=df, spark=spark_session, target_column=target_name,
            dhspark_path=tree_params.dhspark_path,
            data_params=tree_params.data_params
        )
        tree_params.ohe_arr_size_diff = diff_map

        # Handle data with no coreset
        df = df.select(tree_params.calc_column_names)
        self._handle_data_no_coreset(df=df, coreset_tree=coreset_tree, old_max_chunk=old_max_chunk)
        self._save_create_data(coreset_tree=coreset_tree, spark=spark_session)

        # Handle validation data
        coreset_tree = self._handle_validation_data(coreset_tree=coreset_tree, old_max_chunk=old_max_chunk)

        spark_session.sparkContext.setJobDescription("partial_build_preprocess - Save Data")

        # Save data before building the tree
        self._save_validation_and_metadata_for_build(coreset_tree=coreset_tree, spark=spark_session)

    def partial_build_preprocess_from_df(self, spark_session: SparkSession, input_df: DataFrame):
        """
        Creates partial build for an existing coreset tree and adding new data.

        Args:
        - spark_session: SparkSession object.
        - input_df: DataFrame containing new data to add to the tree.        .
        Returns:
        None
        """
        self._partial_build_preprocess(spark_session=spark_session, input_df=input_df)

    def partial_build_preprocess_from_file(self, spark_session: SparkSession, input_path: str,
                                           input_format: str = "parquet"):
        """
        Creates partial build for an existing coreset tree and adding new data.

        Args:
        - spark_session: SparkSession object.
        - input_path: Path to the new data to add to en existing tree.
        - input_format (str) the type of input file/s to read parquet is default csv or json
        Returns:
        None
        """

        source_df = spark_session.read.format(input_format).option("header", "true").option("inferSchema", "true").load(
            input_path)
        self._partial_build_preprocess(spark_session=spark_session, input_df=source_df)

    def _partial_build(self, spark_session: SparkSession, stop_level: int = None):
        """
            Perform a partial build of the coreset tree afture creating the tree data using create_partial_build_data.

            Args:
            - metadata_path: Path to the tree  metadata.
            - spark_session: SparkSession object.
            - stop_level (int) : the level to stop building the tree since the first level needs more cloud resources
            usually we have a step crating the first level (level 0) only and then a step crating the rest of the tree

            Returns:
            None
            """
        # Set the level to 0 and initialize SparkSession
        level = 0

        partial_build = True

        # Load the tree from metadata
        tree = self._load(spark=spark_session, dhspark_path=self._tree_params.dhspark_path)
        tree_params = self._tree_params
        self._init_coreset()
        # support for stop level  to build each level at a different session
        tree_params.stop_level = stop_level
        max_chunk = tree_params.first_level_max_chunk
        if tree_params.stop_level_max_chunk is not None:
            max_chunk = tree_params.stop_level_max_chunk

        spark_session.sparkContext.setJobDescription("partial_build - Create Tree")
        # Calculate coreset tree
        self._calculate_coreset(
            coreset_tree=tree, level=level, max_chunk=max_chunk,
            target_column=tree_params.target_column,
            partial_build=partial_build,
            spark=spark_session, coreset=tree_params.coreset,
            partial_build_starting_index=tree_params.partial_build_starting_index,
            partial_build_old_max_chunk=tree_params.first_level_last_max_chunk
        )

        # Save tree metadata
        spark_session.sparkContext.setJobDescription("partial_build - Save Tree metadata")
        self._save_metadata(coreset_tree=tree, spark=spark_session)

        print("Finish Saving partial tree")

    def partial_build(self, spark_session: SparkSession, stop_level: int = None):
        """
            Perform a partial build of the coreset tree afture creating the tree data using create_partial_build_data.

            Args:
            - spark_session: SparkSession object.
            - stop_level (int) : the level to stop building the tree since the first level needs more cloud resources
            usually we have a step crating the first level (level 0) only and then a step crating the rest of the tree

            Returns:
            None
            """
        self._partial_build(spark_session=spark_session, stop_level=stop_level)

    def _init_coreset(self):
        tree_params = self._tree_params
        tree_params.coreset = self.coreset_cls(**tree_params.coreset_params.to_dict())

    def _calculate_max_chunk_index(self, df, chunk_by=None, last_max_chunk=None):
        """
            Calculates the maximum chunk index based on different chunking strategies and parameters.

            This function supports three different methods of calculating the maximum chunk index:
            1. Based on exact instance count and chunk size
            2. Based on existing chunk indices in the DataFrame where there is no chunk by column
            3. Based on chunk_by column using pandas tree the pandas tree is created as well here

            Args:
                df (DataFrame): Input Spark DataFrame
                chunk_by (str, optional): Column name used for chunking. Defaults to None
                last_max_chunk (int, optional): Previous maximum chunk index for incremental processing.
                    Defaults to None

            Returns:
                int: Maximum chunk index calculated based on the specified strategy
            """
        tree_params = self._tree_params
        if tree_params.n_instances_exact is not None and tree_params.n_instances_exact and tree_params.n_instances is not None and chunk_by is None:
            # manually calculating max chunk with no spark transformations
            max_chunk = (tree_params.n_instances + tree_params.chunk_size - 1) // tree_params.chunk_size
            if last_max_chunk is not None:
                max_chunk = max_chunk + last_max_chunk
        elif chunk_by is None:
            max_chunk = \
                df.select("chunk_index").dropDuplicates(["chunk_index"]).agg(f.max(f"chunk_index")).collect()[0][0]
        else:  # here we also create the pandas tree to by used in the chunk by case with no spark transformations here
            max_chunk = self._create_chunk_by_pandas_tree(self._tree_params.temp_metadata_pd_df, chunk_by)
        return max_chunk

    def _handle_data_no_coreset(self, df: DataFrame, coreset_tree: TreeDataFrame, old_max_chunk=None):
        if old_max_chunk is not None:
            coreset_tree.getChunkDataNoCoreset().level_metadata[
                LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE] = old_max_chunk
            coreset_tree.setChunkDataNoCoresetDF(self._union_no_max_chunk(df, coreset_tree.getChunkDataNoCoresetDF()),
                                                 coreset_tree.getChunkDataNoCoreset().level_metadata)
        else:
            coreset_tree.setChunkDataNoCoresetDF(df)

        return coreset_tree

    def _handle_validation_data(self, coreset_tree: TreeDataFrame, starting_chunk=1, old_max_chunk=None):
        tree_params = self._tree_params
        if tree_params.chunk_sample_ratio > 0:
            if old_max_chunk is not None:
                # do this in case partal build
                df = coreset_tree.getChunkDataNoCoresetDF().where(f.col("chunk_index") > old_max_chunk)
            else:
                df = coreset_tree.getChunkDataNoCoresetDF()
            validation_df = df.sampleBy("chunk_index",
                                        fractions={i: tree_params.chunk_sample_ratio for i in
                                                   range(starting_chunk, tree_params.first_level_max_chunk + 1)},
                                        seed=1234)
            validation_df = validation_df.select(tree_params.calc_column_names)
            if old_max_chunk is not None:
                coreset_tree.getValidation().level_metadata[
                    LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE] = old_max_chunk
                coreset_tree.setValidationDF(self._union_no_max_chunk(validation_df, coreset_tree.getValidationDF()),
                                             coreset_tree.getValidation().level_metadata)
            else:
                coreset_tree.addValidation(validation_df)
        return coreset_tree

    def _select_columns(self, chunk_by, data_params: DataParams, df: DataFrame):
        full_column_list = []
        for f in data_params.features:
            full_column_list.append(f.name)

        target_name = None
        index_name = None
        if data_params.target is not None:
            target_name = data_params.target.name
            full_column_list.append(target_name)
        if data_params.index is not None:
            index_name = data_params.index.name
            full_column_list.append(index_name)
        if chunk_by is not None:
            full_column_list.append(chunk_by)
            # using only original columns:

        # for col in client_cols
        df = df.select(full_column_list)

        return full_column_list, target_name, index_name, df

    def _create_group_by_udf_func_schema(self, df):
        to_append = [StructField(f"sensitivity", DoubleType()), StructField(f"weights", DoubleType())]
        scm = StructType(df.schema.fields + to_append)
        return scm

    def _udf_create_coreset(self,
                            key, pdf, coreset, coreset_size, target_column=None,
                            test_udf_log_path=None,
                            sample_all=None, trace_mode=None,
                            class_size=None, chunk_by_coreset_size_list=None
                            ):
        if trace_mode == TRACE_MODE_VALUES[1] and test_udf_log_path is not None:
            set_udf_logging(test=True, filename=f'{test_udf_log_path}/logs/udf_create_coreset.log')

        if not self.has_categorical():
            X = np.stack(pdf['features'].to_numpy())
        else:
            number_of_numeric = len(self._tree_params.numeric_columns)
            category_lengths = self._get_categories_lengths()
            # Extract numerical features into a dense matrix
            numerical_features = np.vstack([row[:number_of_numeric] for row in pdf["features"]])
            # Extract one-hot indices
            one_hot_indices = np.vstack([row[number_of_numeric:] for row in pdf["features"]])
            X = _get_matrix(
                numerical_data=numerical_features,
                one_hot_indices=one_hot_indices,
                cat_lengths=category_lengths
            )
            if self._get_density(category_lengths) > 0.01:
                X = X.toarray()
        if chunk_by_coreset_size_list is not None:
            chunk_index = key[0] - 1
            coreset_size = int(max(chunk_by_coreset_size_list[chunk_index], 1))
        Y = None
        if target_column is not None and target_column in pdf.columns:
            Y = pdf[target_column].to_numpy()

        w = None
        # we should not pass sensitivities for spark tree
        s = None

        if "weights" in pdf.columns and pdf[f"weights"].notnull().any():
            w = pdf[f"weights"].to_numpy()

        pdf = self._udf_call_build_coreset(
            X=X, Y=Y, coreset=coreset, coreset_size=coreset_size, pdf=pdf, s=s, w=w, trace_mode=trace_mode,
            sample_all=sample_all, class_size=class_size)
        return pdf

    def _udf_call_build_coreset(self,
                                X, Y, coreset, coreset_size, pdf, s, w, trace_mode=None,
                                sample_all=None,
                                class_size=None):
        # return correct type to keys converted to strings
        if Y is not None and len(Y) > 0 and class_size is not None:
            class_size_processed = {}
            y_element = Y[0]
            for class_key in class_size:
                if isinstance(y_element, (int, np.integer)):
                    class_size_processed[int(class_key)] = class_size[class_key]
                elif isinstance(y_element, (float, np.floating)):
                    class_size_processed[float(class_key)] = class_size[class_key]
                else:
                    class_size_processed[class_key] = class_size[class_key]
        else:
            class_size_processed = class_size

        indexes, weights = coreset.build(
            X=X, y=Y, w=w, new_state=s,
            coreset_size=coreset_size, sample_all=sample_all, class_size=class_size_processed)
        if trace_mode == TRACE_MODE_VALUES[1] and len(indexes) == 0:
            logging.info("No indexes return coreset will be Empty")
        w = np.zeros(X.shape[0])
        for i, (in_value, w_value) in enumerate(zip(indexes, weights)):
            w[in_value] = w_value

        pdf[f"sensitivity"] = coreset.sensitivities
        pdf[f"weights"] = w
        # filtering only coreset data
        pdf = pdf[pdf["weights"] != 0]
        return pdf

    def _calculate_coreset(
            self, coreset_tree: TreeDataFrame, level, max_chunk, coreset, spark,
            target_column=None, partial_build=False,
            test_mode: bool = False,
            partial_build_starting_index=None,
            partial_build_old_max_chunk=None
    ):
        tree_params = self._tree_params
        df = coreset_tree.getChunkDataNoCoresetDF()
        leaf_factor = tree_params.leaf_factor
        if self._tree_params.save_orig == SaveOrig.PREPROCESSING_ONLY:
            df = df.select(*[col for col in df.columns if not col.endswith('_original')])

        scm = self._create_group_by_udf_func_schema(df)
        if tree_params.stop_tree_size is not None:
            level = tree_params.stop_tree_size
        # checking if we are on the fist level
        if level == 0:
            # calculating the firest coreset and if there is a root cooreset (orphan) the max chunk will be updated.
            coreset_tree = self._calculate_first_level(
                coreset=coreset, coreset_tree=coreset_tree, df=df,
                level=level,
                max_chunk=max_chunk, leaf_factor=leaf_factor,
                partial_build=partial_build,
                partial_build_old_max_chunk=partial_build_old_max_chunk,
                spark=spark, scm=scm,
                target_column=target_column)
        elif level > 0:
            level -= 1
        # updating metadata if there is stop level
        if tree_params.stop_level is not None:
            tree_params.stop_level_max_chunk = max_chunk
            tree_params.stop_tree_size = level + 1
        min_factor_size = leaf_factor - 1
        # whill the max chunk is more the factor size -1 which is the max chunk for everey level.
        while (max_chunk > min_factor_size):
            if tree_params.stop_level is not None and tree_params.stop_level == level:
                print(f"Stop creating the tree at level {level}")
                break

            level += 1
            print(f"in the loop {max_chunk} factor condition: {min_factor_size} level {level}")
            # calculating the next max chunk
            max_chunk = max_chunk // leaf_factor
            # we need to create a new level we use the old level to create the new
            if not coreset_tree.levelInTree(level):
                to_df = coreset_tree.getLevelDF(level - 1)
                # getting only coresets which can be marged.
                to_df = to_df.where(f.col("chunk_index") <= max_chunk * leaf_factor)
                # merging the coresets
                to_df = to_df.withColumn(f"chunk_index", ((f.col(f"chunk_index") - 1) / leaf_factor).cast("int") + 1)
                # calculating the new coresets.
                to_df = self._calculate_coreset_fields(
                    df=to_df, coreset=coreset, scm=scm,
                    level=level, max_chunk=max_chunk,
                    target_column=target_column)
            else:
                # This is uses in the partal build adding on existing levels.
                # a = datetime.now()
                print(f"Current level in partial build :{level}")
                # creating the new level data fram and the existing (old ) level data frame to get the calculated coresets from.
                new_data_lvl = coreset_tree.getLevel(level - 1)
                old_data_lvl = coreset_tree.getLevel(level)
                new_data_df = new_data_lvl.level_df
                old_data_df = old_data_lvl.level_df
                # marking new data in order to calculate only coreset on new data
                old_max_chunk = self._calculate_chunks_to_move(
                    df=new_data_df, partial_build_starting_index=partial_build_starting_index)
                chunks_to_find = int(old_max_chunk / leaf_factor)
                print(
                    f"up to chunk {old_max_chunk} can be taken from old data,check id to find in old data {chunks_to_find}")
                chunks_to_move_df = old_data_df.where(f.col("chunk_index") <= chunks_to_find)
                old_data_lvl.level_metadata[LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE] = chunks_to_find
                # to remove corersets which are orphans to move
                new_data_df = new_data_df.where(f.col("chunk_index") <= (max_chunk * leaf_factor))

                new_data_df = new_data_df.where(f.col("chunk_index") > (chunks_to_find * leaf_factor))
                # no data  to calculate finish the tree the level is empty.
                if new_data_df.rdd.isEmpty():
                    print("the new data frame is empty no need to continue calculation")
                    break

                # marging the corsets.
                new_data_df = new_data_df.withColumn(f"chunk_index",
                                                     ((f.col(f"chunk_index") - 1) / leaf_factor).cast("int") + 1)

                new_data_df = self._calculate_coreset_fields(
                    df=new_data_df, coreset=coreset, scm=scm,
                    level=level,
                    max_chunk=max_chunk,
                    target_column=target_column)
                # finish calculating the coreset unmarking new data

                u_df = self._union_df_fix_chunk_id(
                    df1=chunks_to_move_df, df2=new_data_df, level=level,
                    leaf_factor=leaf_factor, max_chunk=max_chunk)

                to_df = u_df

            print(f"adding level {level}")
            coreset_tree = self._save_level(df=to_df, tree=coreset_tree, level=level,
                                            spark=spark)
            if tree_params.stop_level is not None:
                tree_params.stop_level_max_chunk = max_chunk
                tree_params.stop_tree_size = level + 1

        print("finish bulling tree")

        # cleaning the stop level variable to be used again. in anather parthal build.
        if tree_params.stop_tree_size is not None and max_chunk <= min_factor_size:
            print("cleaning the stop values  ")
            tree_params.stop_tree_size = None
            tree_params.stop_level_max_chunk = None
        return coreset_tree

    def _calculate_first_level(self, coreset, coreset_tree: TreeDataFrame, df: DataFrame, level, leaf_factor, max_chunk,
                               partial_build,
                               partial_build_old_max_chunk,
                               spark, scm, target_column):
        if partial_build:
            df = df.where(f.col("chunk_index") > partial_build_old_max_chunk)

        df = self._calculate_coreset_fields(
            df=df, coreset=coreset, scm=scm, level=level,
            max_chunk=max_chunk, target_column=target_column)

        if partial_build:
            level_df = coreset_tree.getLevelDF(level)
            df = self._union_df_fix_chunk_id(
                df1=level_df, df2=df, level=level,
                leaf_factor=leaf_factor,
                max_chunk=max_chunk)
            # calculating the partial build partation to add
            if partial_build_old_max_chunk % leaf_factor > 0:
                coreset_tree.getLevel(level).level_metadata[
                    LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE] = partial_build_old_max_chunk - (
                        leaf_factor - 1)
            else:
                coreset_tree.getLevel(level).level_metadata[
                    LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE] = partial_build_old_max_chunk
        coreset_tree = self._save_level(df=df, tree=coreset_tree, level=level, spark=spark)
        return coreset_tree

    def _calculate_chunks_to_move(self, df: DataFrame, partial_build_starting_index):
        if self._tree_params.partial_build_ending_chunk_by is None:
            df = df.withColumn("should_rebuild_coreset",
                               f.when(f.col("row_index_id") >= partial_build_starting_index,
                                      f.lit(1)).otherwise(
                                   f.lit(0)))
        else:
            df = df.withColumn("should_rebuild_coreset",
                               f.when(
                                   f.col(self._tree_params.chunk_by) > self._tree_params.partial_build_ending_chunk_by,
                                   f.lit(1)).otherwise(
                                   f.lit(0)))

        grouped_df = df.groupBy('chunk_index').agg(f.sum('should_rebuild_coreset').alias('sum_rebuild_coreset'))
        chunk_to_move = grouped_df.where(f.col("sum_rebuild_coreset") == 0).select(f.max("chunk_index")).collect()[0][0]
        return chunk_to_move

    def _union_df_fix_chunk_id(self, df1, df2, level, leaf_factor, max_chunk):
        to_df = self._union_no_max_chunk(df1, df2)
        # print(f"using exiting max chunk :{max_chunk}")
        to_df = to_df.withColumn("level", f.lit(level).cast("int"))
        return to_df

    def _union_no_max_chunk(self, df1, df2):
        df1 = df1.select(df2.columns)
        to_df = df1.union(df2)
        return to_df

    def _calculate_coreset_fields(self, df, scm, level, max_chunk, coreset, target_column=None):
        tree_params = self._tree_params
        coreset_size = tree_params.coreset_size

        dhspark_path = tree_params.dhspark_path
        # fair = tree_params.fair
        sample_all = tree_params.sample_all
        class_size = tree_params.class_size
        # deterministic_size = tree_params.deterministic_size
        # in case we use chunk by
        chunk_by_coreset_sizes = None
        if tree_params.chunk_by_tree is not None:
            chunk_by_coreset_sizes = (tree_params.chunk_by_tree[level]["coreset_size"]).to_list()

        if isinstance(coreset_size, dict):
            if class_size is not None:
                raise RuntimeError('It is not allowed to use class_size at the same '
                                   'time as passing class sizes through coreset_size')
            class_size = coreset_size
            coreset_size = None

        elif isinstance(coreset_size, (float, np.floating)) and tree_params.chunk_size is not None:
            coreset_size = int(max(coreset_size * tree_params.chunk_size, 2))

        def _create_coreset_udf(key, pdf):
            return self._udf_create_coreset(key=key, pdf=pdf, coreset=coreset, coreset_size=coreset_size,
                                            target_column=target_column,
                                            trace_mode=tree_params.trace_mode, test_udf_log_path=dhspark_path,
                                            sample_all=sample_all,
                                            class_size=class_size, chunk_by_coreset_size_list=chunk_by_coreset_sizes)

        df = df.coalesce(max_chunk).groupby(f"chunk_index").applyInPandas(_create_coreset_udf, schema=scm)
        df = df.withColumn("level", f.lit(level).cast("int"))
        return df

    def _create_index_and_chunk(self, chunk_size, level, df, index_start=1, chunk_by=None,
                                chunk_start=1, index_column=None):
        """
           Creates chunks of data and adds indexing columns to a Spark DataFrame.
           The function prepares the data to build the coresets
           This function supports two chunking strategies:
           1. Size-based chunking: Splits data into chunks of specified size
           2. Column-based chunking: Splits data based on unique values in a specified column

           Args:
               chunk_size (int): Number of rows per chunk when using size-based chunking
               level (int): Tree level identifier for hierarchical processing (now only 0)
               df (pyspark.sql.DataFrame): Input DataFrame to be chunked
               index_start (int, optional): Starting value for row indexing. Defaults to 1
               chunk_by (str, optional): Column name to chunk by. Defaults to None
               chunk_start (int, optional): Starting value for chunk indexing. Defaults to 1
               index_column (str, optional): Existing column to use as row index. Defaults to None

           Returns:
               tuple: (DataFrame with added chunking columns, list of calculated column names)

           Raises:
               Exception: If neither chunk_size nor chunk_by is provided
           """

        calculated_column_names_arr = []  # adding new created columns
        # Validate chunking parameters
        if chunk_by is None and chunk_size is None:
            raise Exception("Either chunk_size or chunk_by must be provided.")
        if chunk_by is None:
            # Size-based chunking strategy
            if index_column is None:
                # Create row indices if no index column provided
                df = df.rdd.zipWithIndex().toDF()
                df = df.select(f.col("_1.*"), (f.col("_2") + index_start).alias('row_index_id'))
            else:
                df = df.withColumn(f"row_index_id", f.col(index_column))
            # this change we have the ceil(): which ensures each chunk of chunk size rows gets a unique chunk ID.
            # Calculate chunk index using ceiling division to ensure even distribution
            df = df.withColumn(f"chunk_index", f.ceil((f.col("row_index_id") - (index_start - 1)) / chunk_size) + f.lit(
                chunk_start - 1))

            calculated_column_names_arr.append("row_index_id")
            print("first chunking of the data and adding validation columns")
        else:
            # Column-based chunking strategy -  Handle chunk by column
            df = df.repartition(chunk_by)  # reparation the data to get better performance
            # Create sub-chunks if chunk_size is specified
            if chunk_size is not None:
                df = self._create_chunk_by_sub_chunks(chunk_by, chunk_size, df)

            # Calculate coreset size for each chunk and creating the group by data for the chunk by tree methdata
            group_df = df.groupBy(chunk_by).agg(
                f.floor(f.count("*") * self._tree_params.coreset_size).alias("coreset_size")).orderBy(chunk_by,
                                                                                                      ascending=True)
            group_df = group_df.persist()

            self._tree_params.temp_metadata_pd_df = group_df.toPandas()
            # Create chunk indices small df with chunk_index and chunk by column
            chunk_df = group_df.select(chunk_by).rdd.zipWithIndex().toDF()
            chunk_df = chunk_df.select(f.col("_1.*"), (f.col("_2") + chunk_start).alias('chunk_index'))
            # Join chunk indices back to main DataFrame
            df = df.join(f.broadcast(chunk_df), df[chunk_by] == chunk_df[chunk_by]).select(df['*'], chunk_df[
                "chunk_index"])
            group_df.unpersist()

            calculated_column_names_arr.append(chunk_by)
        # add level column
        df = df.withColumn(f"level", f.lit(level))
        # reparation the data by chunk index for better performance
        df = df.repartition("chunk_index")
        calculated_column_names_arr = calculated_column_names_arr + ["chunk_index", "level"]

        return df, calculated_column_names_arr

    def _create_chunk_by_sub_chunks(self, chunk_by, chunk_size, df):
        # using window function only with in the partitions
        window_spec = Window.partitionBy(chunk_by).orderBy(chunk_by)
        # Add a row number column
        df_with_row_num = df.withColumn("row_num", f.row_number().over(window_spec))
        # Calculate the chunk_id by dividing row_num by chunk size and taking the ceiling
        df_with_schunks = df_with_row_num.withColumn("sub_chunk_id",
                                                     ((df_with_row_num[f"row_num"] - 1) / chunk_size).cast("int") + 1)
        # crating a new chunk by column which is split to more chunks
        df_chunk_by = df_with_schunks.withColumn(
            f"{chunk_by}_tmp",
            f.when(
                f.col("sub_chunk_id") > 1,
                f.concat(f.col(chunk_by), f.lit(SUB_CHUNK_PREFIX), f.col("sub_chunk_id"))
            ).otherwise(f.col(chunk_by))
        )
        df = df_chunk_by.drop("sub_chunk_id")
        df = df.drop(chunk_by).withColumnRenamed(f"{chunk_by}_tmp", chunk_by)

        return df

    def _data_preprocess_transformers(
            self, df, spark, target_column,
            dhspark_path,
            output_features_column_name="features",
            data_params=None):
        """
            Preprocesses data by applying transformations to categorical and target columns.

            This function handles:
            - String indexing for categorical features
            - One-hot encoding for categorical features
            - Target column encoding (if string type)
            - Feature column creation

            Args:
                df (pyspark.sql.DataFrame): Input DataFrame
                spark (SparkSession): Active Spark session
                target_column (str): Name of the target/label column
                dhspark_path (str): Path for persisting category indexer
                output_features_column_name (str, optional): Name for the output features column.
                    Defaults to "features"
                data_params (object, optional): Parameters object containing settings for all columns

            Returns: tuple: (
                    Preprocessed DataFrame,
                    Dictionary of maximum differences,
                    Output target column name,
                    List of transformer column names
                )
            """

        transformer_columns = []
        transformers_list = []
        y_output_column = target_column
        columns_data_types = dict(df.dtypes)
        if self._tree_params.categorical_columns is not None and len(self._tree_params.categorical_columns) > 0:
            df = df.cache()
        if data_params is None or data_params.ohe_max_categories is None:
            ohe_max_categories = 100
        else:
            ohe_max_categories = data_params.ohe_max_categories

        # Create string indexer transformer  for categorical features
        indexer = PersistStringIndexer(
            input_columns=self._tree_params.categorical_columns,
            output_column_suffix='_index',
            saved_category_path=dhspark_path,
            spark=spark,
            max_category_size=ohe_max_categories,
        )
        transformers_list.append(indexer)
        # Handle string target column if present adding string indexer for target column
        is_target_column_string = columns_data_types[target_column] == "string"
        if target_column is not None and is_target_column_string:
            y_output_column = target_column + "_index"
            y_indexer = PersistStringIndexer(
                input_columns=[target_column], output_column_suffix='_index',
                saved_category_path=dhspark_path, spark=spark)
            transformers_list.append(y_indexer)

        # Execute The string indexer transformers
        df = self._execute_pipline(df, transformers_list)
        df = self._create_features_column(
            data_df=df,
            features_column_name=output_features_column_name
        )
        max_diff_map = indexer.max_map
        result_tuple = df, max_diff_map, y_output_column
        result_tuple = result_tuple + (transformer_columns + [output_features_column_name],)

        if self._tree_params.save_orig != SaveOrig.NONE:
            result_tuple = (result_tuple[:-1] +
                            (result_tuple[-1] +
                             [col + '_original' for col in self._tree_params.numeric_columns] +
                             [col + '_original' for col in self._tree_params.categorical_columns],))
        return result_tuple

    def _execute_pipline(self, df, transformers_list):
        pipline = Pipeline(stages=transformers_list)
        pip_model = pipline.fit(df)
        df = pip_model.transform(df)
        return df

    def _get_categories_lengths(self):
        """
        Function returns list of number of values for categorical features.
        len(result) = number of categorical features.
        For example, for the dataset below we should return [3, 2]
        ----------------------
        num_1 cat_1 cat_2
        ----------------------
          1     A     D
          5     B     F
          5     C     F
        ----------------------
        If number of values > ohe_max_categories, for such feature we return exactly ohe_max_categories
        """
        full_categories_loaded = pd.read_parquet(
            os.path.join(self._tree_params.dhspark_path, 'string_indexer', 'all', 'categories.parquet')
        )
        # filter out target values
        target_column = self._tree_params.target_column or self._tree_params.data_params.target.name
        full_categories_loaded = full_categories_loaded[
            full_categories_loaded['name'] != target_column.replace('_index', '')]
        # for each category count number of values
        categories_lengths = [len(r[1]) + 1 for r in full_categories_loaded.to_numpy()]
        return categories_lengths

    def _get_output_features(self):
        """
        Function returns list of output features after OHE
        For example, for the dataset below we should return
        ['num_1', 'cat_1_A', 'cat_1_B', 'cat_1_C', 'cat_2_D', 'cat_2_F']
        ----------------------
        num_1 cat_1 cat_2
        ----------------------
          1     A     D
          5     B     F
          5     C     F
        ----------------------
        """
        output_features = self._tree_params.numeric_columns
        if self.has_categorical():
            full_categories_loaded = pd.read_parquet(
                os.path.join(self._tree_params.dhspark_path, 'string_indexer', 'all', 'categories.parquet')
            )
            # filter out target values
            target_column = self._tree_params.target_column or self._tree_params.data_params.target.name
            full_categories_loaded = full_categories_loaded[
                full_categories_loaded['name'] != target_column.replace('_index', '')]
            for cat in self._tree_params.categorical_columns:
                output_features += [cat + '_infrequent']
                output_features += [cat + '_' + field for field
                                    in full_categories_loaded[full_categories_loaded['name'] == cat].iloc[0, 1]
                                    ]

        return output_features

    def _create_features_column(self, data_df, features_column_name):
        all_columns = (self._tree_params.numeric_columns +
                       [col + '_index' for col in self._tree_params.categorical_columns])
        data_df = data_df.withColumn(
            features_column_name,
            f.array(*all_columns)
        )
        return data_df

    def _handle_missing_values_params(self, df: DataFrame, categorical_only: bool = False):
        """
               Handles missing values in a DataFrame based on provided DataParams configuration.

               This function processes both categorical and numeric features, applying different
               filling strategies including:
               - Constant values for categorical features
               - Constant values, mean, median, or mode for numeric features
        """

        data_params = self._tree_params.data_params
        if self._tree_params.save_orig != SaveOrig.NONE:
            for column in self._tree_params.numeric_columns + self._tree_params.categorical_columns:
                df = df.withColumn(f'{column}_original', sqlf.col(column))
        categorical_map = {}
        feature_numeric_map = {}
        inputer_map = {}
        # Process features from data_params and set appropriate fill values creating numeric and categorical map
        # splitting data params features
        for f in data_params.features:
            if f.categorical:
                if f.fill_value is None:
                    f.fill_value = data_params.fill_value_cat
                categorical_map[f.name] = f
            else:
                if f.fill_value is None:
                    f.fill_value = data_params.fill_value_num
                feature_numeric_map[f.name] = f
            if data_params.categorical_features is not None:
                for c_f in data_params.categorical_features:
                    if c_f not in categorical_map:  # adding categorical feature if not defined for a specific field.
                        categorical_map[c_f] = FeatureField(c_f, None, None, True, data_params.fill_value_cat)

        # Handle categorical features replacing null categorical values
        for c_name, value in categorical_map.items():
            if value is not None:
                df = df.na.fill(value.fill_value, c_name)

        if not categorical_only:
            for name, value in feature_numeric_map.items():
                if value is not None:
                    if value.fill_value == "mean" or value.fill_value == "median" or value.fill_value == "mode":
                        if value.fill_value not in inputer_map:
                            inputer_map[value.fill_value] = []
                        inputer_map[value.fill_value].append(name)
                    elif value is not None and value.fill_value is not None:
                        df = df.na.fill(value.fill_value, name)
        for key, value in inputer_map.items():
            df = self._execute_imputer(value, df, key)

        return df

    def _execute_imputer(self, imputer_column_names, missing_df, strategy="mean"):
        if len(imputer_column_names) > 0:
            imputer = Imputer(inputCols=imputer_column_names, outputCols=imputer_column_names, strategy=strategy)
            missing_df = imputer.fit(missing_df).transform(missing_df)
        return missing_df

    def _save_level(self, df, tree: TreeDataFrame, level: int, spark: SparkSession):
        spark.sparkContext.setJobDescription(f"build/partial_build - Save Level {level}")
        tree_params = self._tree_params
        save_path = os.path.join(tree_params.dhspark_path, "tree")
        print(f"Saving Level {level} to {save_path}")
        level_df = tree.addUpdateLevel(level)
        partitions_to_save = level_df.level_metadata.get(LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE)
        root_coreset_partition = level_df.level_metadata.get(LevelDataFrame.MetaDataParams.ROOT_CORESET_PARTITION)
        if df is not None:
            if partitions_to_save is not None:
                saved_partitions = partitions_to_save
                if root_coreset_partition is not None:
                    root_coreset_partition = root_coreset_partition - 1
                    if root_coreset_partition < saved_partitions:
                        saved_partitions = root_coreset_partition

                df = df.where(f.col("chunk_index") > saved_partitions)

            df.write.partitionBy('level', 'chunk_index').option(
                "partitionOverwriteMode", "dynamic").save(
                mode="overwrite", format="parquet",
                path=save_path)
            df = spark.read.option("basePath", save_path).format("parquet").load(save_path).filter(f"level=={level}")
            tree.addUpdateLevel(level, df)
        return tree

    def _save_create_data(self, coreset_tree: TreeDataFrame, spark: SparkSession):
        tree_params = self._tree_params
        save_path = os.path.join(tree_params.dhspark_path, "create_tree_data")
        spark.sparkContext.setJobDescription("build_preprocess/partial_build_preprocess - Save Data")
        print(f"Saving Level no_coreset to {save_path}")

        df = coreset_tree.getChunkDataNoCoresetDF()
        partition_to_save = coreset_tree.getChunkDataNoCoreset().level_metadata.get(
            LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE)
        print(f"Saving create data tree in {save_path}- partition to save {partition_to_save}")
        if partition_to_save is not None:
            df = df.where(f.col("chunk_index") > partition_to_save)
        df.write.partitionBy('chunk_index').option(
            "partitionOverwriteMode", "dynamic").save(
            mode="overwrite", format="parquet",
            path=save_path)
        df = spark.read.option("basePath", save_path).format("parquet").load(save_path)
        coreset_tree.setChunkDataNoCoresetDF(df)
        return coreset_tree

    def _save_validation_and_metadata_for_build(self, coreset_tree: TreeDataFrame, spark: SparkSession):
        if self._tree_params.first_level_max_chunk > 0:
            print("Saving data validation data and metadata before building tree")
            # spark.sparkContext.setJobDescription("build_preprocess/partial_build_preprocess - Save Data")
            # self._save_create_data(coreset_tree=coreset_tree, spark=spark)
            spark.sparkContext.setJobDescription("build_preprocess/partial_build_preprocess - Save Validation Data")
            self._save_validation_data(coreset_tree)
            spark.sparkContext.setJobDescription("build_preprocess/partial_build_preprocess - Save Meta Data")
            self._save_metadata(coreset_tree=coreset_tree, spark=spark)
        return coreset_tree

    def _chunk_tree_to_json(self):
        tree_params = self._tree_params
        json_data = None
        if tree_params.chunk_by is not None:
            data_params = tree_params.data_params
            chunk_by_format = data_params.seq_column.get("datetime_format")
            df_combined = pd.concat(tree_params.chunk_by_tree)
            # Format the date columns as strings with a specific format
            df_combined['start_seq'] = df_combined['start_seq'].dt.strftime(chunk_by_format)
            df_combined['end_seq'] = df_combined['end_seq'].dt.strftime(chunk_by_format)
            # Convert the combined DataFrame to JSON
            json_data = df_combined.to_json(orient='records')
        return json_data

    def _chunk_tree_from_json(self, json_tree):
        dfs = None
        if json_tree is not None:
            # Convert JSON back to a pandas DataFrame
            df_from_json = pd.read_json(json_tree)

            # If needed, convert the date columns back to Timestamp
            df_from_json['start_seq'] = pd.to_datetime(df_from_json['start_seq'])
            df_from_json['end_seq'] = pd.to_datetime(df_from_json['end_seq'])

            # Split the DataFrame back into an array of DataFrames based on 'level' column
            grouped = df_from_json.groupby('level')
            dfs = [group for _, group in grouped]
        return dfs

    def _save_metadata(self, coreset_tree: TreeDataFrame, spark: SparkSession):
        tree_params = self._tree_params
        if tree_params.first_level_max_chunk is not None and tree_params.first_level_max_chunk > 0:
            dhspark_path = os.path.join(tree_params.dhspark_path, "tree_metadata")
            print(f"Saving the metadata in {dhspark_path} ")
            partial_build_ending_chunk_by = None
            if tree_params.partial_build_ending_chunk_by is not None:
                partial_build_ending_chunk_by = str(tree_params.partial_build_ending_chunk_by)
            data = [
                {
                    "first_level_max_chunk": tree_params.first_level_max_chunk,
                    "first_level_last_max_chunk": tree_params.first_level_last_max_chunk,
                    "partial_build_starting_index": tree_params.partial_build_starting_index,
                    "partial_build_ending_chunk_by": partial_build_ending_chunk_by,
                    "chunk_size": tree_params.chunk_size,
                    "coreset_size": json.dumps(tree_params.coreset_size),
                    "leaf_factor": tree_params.leaf_factor,
                    "chunk_sample_ratio": tree_params.chunk_sample_ratio,
                    "n_instances": tree_params.n_instances,
                    "n_instances_exact": tree_params.n_instances_exact,
                    "dhspark_path": tree_params.dhspark_path,
                    "categorical_columns": tree_params.categorical_columns,
                    "numeric_columns": tree_params.numeric_columns,
                    "calc_column_names": tree_params.calc_column_names,
                    "ohe_arr_size_diff": tree_params.ohe_arr_size_diff,
                    "target_column": tree_params.target_column,
                    "chunk_by": tree_params.chunk_by,
                    "index_column": tree_params.index_column,
                    "tree_size": coreset_tree.getTreeSize(),
                    "stop_level_max_chunk": tree_params.stop_level_max_chunk,
                    "stop_level": tree_params.stop_level,
                    "stop_tree_size": tree_params.stop_tree_size,
                    "model_class": tree_params.model_class,
                    "data_params": json.dumps(DataParams.to_dict(tree_params.data_params)),
                    "class_size": json.dumps(tree_params.class_size),
                    "sample_all": json.dumps(tree_params.sample_all),
                    "chunk_by_tree": self._chunk_tree_to_json(),
                    "coreset_params": json.dumps(CoresetParams.to_dict(tree_params.coreset_params)),
                    "save_orig": int(tree_params.save_orig),
                }
            ]
            schema = StructType([
                StructField("tree_size", IntegerType(), True),
                StructField("first_level_max_chunk", IntegerType(), True),
                StructField("first_level_last_max_chunk", IntegerType(), True),
                StructField("partial_build_starting_index", IntegerType(), True),
                StructField("partial_build_ending_chunk_by", StringType(), True),
                StructField("chunk_size", IntegerType(), True),
                StructField("coreset_size", StringType(), True),
                StructField("leaf_factor", IntegerType(), True),
                StructField("chunk_sample_ratio", DoubleType(), True),
                StructField("n_instances", IntegerType(), True),
                StructField("n_instances_exact", BooleanType(), True),
                StructField("target_column", StringType(), True),
                StructField("dhspark_path", StringType(), True),
                StructField("numeric_columns", ArrayType(StringType()), True),  # List field
                StructField("categorical_columns", ArrayType(StringType()), True),  # List field
                StructField("calc_column_names", ArrayType(StringType()), True),  # List field
                StructField("ohe_arr_size_diff", MapType(StringType(), IntegerType()), True),  # Dictionary field
                StructField("data_params", StringType(), True),  # Dictionary field
                StructField("chunk_by", StringType(), True),
                StructField("index_column", StringType(), True),
                StructField("stop_level_max_chunk", IntegerType(), True),
                StructField("stop_tree_size", IntegerType(), True),
                StructField("stop_level", IntegerType(), True),
                StructField("model_class", StringType(), True),
                StructField("class_size", StringType(), True),
                StructField("sample_all", StringType(), True),
                StructField("chunk_by_tree", StringType(), True),  # json field
                StructField("coreset_params", StringType(), True),  # Dictionary field
                StructField("save_orig", IntegerType(), True),
            ])

            df = spark.createDataFrame(data, schema)
            df.coalesce(1).write.save(
                mode="overwrite", format="parquet",
                path=dhspark_path)

    def _save_validation_data(self, coreset_tree: TreeDataFrame):
        save_valid_path = os.path.join(self._tree_params.dhspark_path
                                       , "validation")
        if coreset_tree.getValidation() is not None:
            df = coreset_tree.getValidationDF()
            partition_to_save = coreset_tree.getValidation().level_metadata.get(
                LevelDataFrame.MetaDataParams.PARTITIONS_TO_SAVE)
            print(f"Saving validation in {save_valid_path}- partition to save {partition_to_save}")

            if partition_to_save is not None:
                df = df.where(f.col("chunk_index") > partition_to_save)
            df.write.partitionBy('chunk_index').option(
                "partitionOverwriteMode", "dynamic").save(
                mode="overwrite", format="parquet",
                path=save_valid_path)

    def _load(self, spark: SparkSession, dhspark_path: str) -> TreeDataFrame:
        spark.sparkContext.setJobDescription("_load - Load Tree and Metadata")
        print(dhspark_path)
        load_path = os.path.join(dhspark_path, "tree")
        load_valid_path = os.path.join(dhspark_path, "validation")
        tree_dhspark_path = os.path.join(dhspark_path, "tree_metadata")
        index_data_path = os.path.join(dhspark_path, "index_data")
        create_tree_data_path = os.path.join(dhspark_path, "create_tree_data")
        # getting tree metadata
        spark.sparkContext.setJobDescription("_load - Get Tree Metadata")
        row = spark.read.parquet(tree_dhspark_path).collect()[0]

        data_params_ = row["data_params"]
        data_p = None
        if data_params_ is not None:
            data_p = DataParams.from_dict(json.loads(data_params_))
        coreset_params_ = row["coreset_params"]
        coreset_params = None
        if coreset_params_ is not None:
            coreset_p = json.loads(coreset_params_)
            coreset_params = self.coreset_params_cls(**coreset_p)
        self._tree_params = TreeParams(dhspark_path=dhspark_path, chunk_size=row["chunk_size"],
                                       coreset_size=json.loads(row["coreset_size"]),
                                       chunk_sample_ratio=self._tree_params.chunk_sample_ratio or row[
                                           "chunk_sample_ratio"],
                                       n_instances=self._tree_params.n_instances or row["n_instances"],
                                       n_instances_exact=self._tree_params.n_instances_exact or row[
                                           "n_instances_exact"],
                                       data_params=data_p,
                                       index_column=row["index_column"], chunk_by=row["chunk_by"],
                                       leaf_factor=row["leaf_factor"],
                                       stop_level_max_chunk=row["stop_level_max_chunk"], stop_level=row["stop_level"],
                                       stop_tree_size=row["stop_tree_size"],
                                       first_level_max_chunk=row["first_level_max_chunk"],
                                       first_level_last_max_chunk=row["first_level_last_max_chunk"],
                                       partial_build_starting_index=row["partial_build_starting_index"],
                                       partial_build_ending_chunk_by=row["partial_build_ending_chunk_by"],
                                       target_column=row["target_column"],
                                       numeric_columns=row["numeric_columns"],
                                       categorical_columns=row["categorical_columns"],
                                       calc_column_names=row["calc_column_names"],
                                       ohe_arr_size_diff=row["ohe_arr_size_diff"],
                                       model_class=row['model_class'],
                                       class_size=json.loads(row["class_size"]),
                                       sample_all=json.loads(row["sample_all"]),
                                       chunk_by_tree=self._chunk_tree_from_json(row["chunk_by_tree"]),
                                       coreset_params=coreset_params,
                                       save_orig=row["save_orig"]
                                       )
        self._set_trace_mode(spark_session=spark)
        coreset_tree = TreeDataFrame(tree_params=self._tree_params)

        if self._tree_params.first_level_max_chunk is not None and self._tree_params.first_level_max_chunk > 0:
            coreset_tree.setChunkDataNoCoresetDF(spark.read.format("parquet").load(create_tree_data_path))

        if self._tree_params.chunk_sample_ratio > 0:
            coreset_tree.addValidation(spark.read.format("parquet").load(load_valid_path))

        tree_size = row["tree_size"]

        if tree_size is not None and tree_size > 0:
            print(f"loading tree with max level of {tree_size}  ")
            unified_df = spark.read.option("basePath", load_path).format("parquet").load(load_path)
            for level in range(0, tree_size):
                coreset_tree.addUpdateLevel(level, unified_df.where(f.col("level") == level))

        return coreset_tree

    def fit(self, spark_session: SparkSession, transformer_cls, level: int = 0, seq_from=None, seq_to=None,
            **model_params):
        """
            Fit a classification model and save it along with metadata.

            Args:
                spark_session (SparkSession): The Spark session.

                transformer_cls (type): The  model spark transformer type class to instantiate and fit to get the model.
                level (int, optional): The level in the coreset tree to retrieve the coreset. Defaults to 0.
                seq_from: string/datetime, optional The starting sequence of the training set.
                seq_to : string/datetime, optional The ending sequence of the training set.
                **model_params: Additional parameters for the transformer.

            Returns:
                Model: The fitted model object.
            """
        dhspark_path = self._tree_params.dhspark_path
        model_path = os.path.join(dhspark_path, "model")

        tree = self._load(spark=spark_session, dhspark_path=dhspark_path)
        tree_params = self._tree_params
        if transformer_cls is not None:
            coreset_df = self._retrieve_coreset(tree=tree, level=level, spark=spark_session, seq_from=seq_from,
                                                seq_to=seq_to)
            coreset_df = coreset_df.withColumn("features", mf.array_to_vector("features"))
            # Initialize the fit transformer with provided parameters
            transformer = transformer_cls(featuresCol="features", labelCol=tree_params.target_column,
                                          **model_params)

            model = transformer.fit(coreset_df)
            tree_params.model_class = get_fully_qualified_name(model.__class__)
            spark_session.sparkContext.setJobDescription("fit - Save model Data")
            model.write().overwrite().save(model_path)
            self._save_metadata(coreset_tree=tree, spark=spark_session)
            return self.get_model(spark_session=spark_session)
        else:
            print(f"no model was chosen: {transformer_cls}")
            return None

    def get_model(self, spark_session: SparkSession, save_path=None):
        """
            Load a saved model from metadata and optionally save it to a new path.

            Args:
                spark_session (SparkSession): The Spark session.
                save_path (str, optional): The path to save the loaded model outside the coreset tree. Defaults to None.

            Returns:
                Model: The loaded model object.
            """
        dhspark_path = self._tree_params.dhspark_path
        model_path = os.path.join(dhspark_path, "model")

        tree = self._load(spark=spark_session, dhspark_path=dhspark_path)
        tree_params = self._tree_params
        model = None
        if tree_params.model_class is not None:
            model_class = get_class_from_fully_qualified_name(tree_params.model_class)
            model = model_class.load(model_path)
        if save_path is not None and model is not None:
            model.save(save_path)

        return model

    def _get_orphan_for_level(self, n_leaves, level, leaf_factor):
        """
        Get list of orhan heads for certain level of the tree. Level=0 regarded as leaf level.
        return a list of tuples (level_index, chunk_index), both indexes are starting from 0

        We are suggesting that level - is level of coreset that we are interested in.
        Therefore, all orphans are taken from levels below 'level' (closer to the leaves).
        """
        # list of levels, starting from leaf (index=0), ending on root.
        # for each level element represents a number of nodes
        level_n_nodes = [n_leaves]
        while level_n_nodes[-1] > 1:
            level_n_nodes.append(level_n_nodes[-1] // leaf_factor)
        # collect all orphan nodes (all nodes that do not have 'parent')
        orphan_nodes = []
        for level_index, node_count in enumerate(level_n_nodes):
            if level_index < len(level_n_nodes) - 1:
                # for leaf_factor > 2 there are could be more than one orphan node on the level
                for node_shift_index in range(node_count % leaf_factor):
                    orphan_nodes.append((level_index, node_count - 1 + node_shift_index))
        # all orphans from below levels
        return [node for node in orphan_nodes if node[0] < level]

    def _split_and_process_df(self, df, preprocessing_stage, tree):
        """
        Splitting features column to separate columns.
        Fill features with pre-saved original values when necessary
        Get rid of "features" column.
        We use it for get_coreset processing only
        """
        # split features to separate columns
        df = self._split_features(df)
        # decode target if ot was string-indexed
        if preprocessing_stage != PreprocessingStage.AUTO:
            df = self._decode_target(df)

        # join with leaf data if necessary - in case when we did not save original data on every level
        if (
                self._tree_params.save_orig == SaveOrig.PREPROCESSING_ONLY
                and
                (
                        preprocessing_stage == PreprocessingStage.USER
                        or
                        (preprocessing_stage == PreprocessingStage.USER_NO_MISSING_VALUES and self.has_categorical())
                )
        ):
            if self._tree_params.chunk_by is not None:
                raise RuntimeError('When using chunk_by option simultaneously with '
                                   'preprocessing_stage = PreprocessingStage.USER or '
                                   'PreprocessingStage.USER_NO_MISSING_VALUES '
                                   ' using save_orig = SaveOrig.PREPROCESSING_AND_BUILD is necessary')
            df = df.drop(self._tree_params.target_column, 'level', 'features', 'chunk_index')
            df_chunks = tree.getChunkDataNoCoresetDF()
            df = df.join(df_chunks, on='row_index_id')
            df = df.drop('features')

        # for USER mode restore original data both for numeric and categorical data
        if preprocessing_stage == PreprocessingStage.USER:
            df = df.drop(*(self._tree_params.numeric_columns + self._tree_params.categorical_columns))
            for column in self._tree_params.numeric_columns + self._tree_params.categorical_columns:
                df = df.withColumnRenamed(column + '_original', column)

        # for USER_NO_MISSING_VALUES restore original data only for categorical.
        # No need to do the same for numeric features, we need values after missing values processing
        if preprocessing_stage == PreprocessingStage.USER_NO_MISSING_VALUES and self.has_categorical():
            df = df.drop(*self._tree_params.categorical_columns)
            for column in self._tree_params.categorical_columns:
                df = df.withColumnRenamed(column + '_original', column)
            df = self._handle_missing_values_params(df=df, categorical_only=True)
        df = df.withColumnRenamed('weights', 'w')
        return df

    def _get_density(self, categories_lengths):
        """
        Get estimation of data density after OHE without analyzing the data itself.
        The estimation based on number of values for  categorical features.
        For example:
        ----------------------
        num_1 cat_1 cat_2
        ----------------------
          1     A     D
          5     B     F
          5     C     F
        ----------------------
        numeric sub-dataset we regarding as having density 1 (in real life it's correct of there is no zeros).
        after OHE we will have such data -
        ----------------------
          1   1 0 0    1 0
          5   0 1 0    0 1
          5   0 0 1    0 1
        ----------------------
        density = (number of non-zero values) / (number of values)
        therefore, for each row of data  density = (num_of_categorical + num_of_numeric) / (number of output features after OHE)
        therefore, for the while dataset density = density of any row.
        """
        if categories_lengths is None:
            categories_lengths = self._get_categories_lengths()
        if len(categories_lengths) == 0:
            density = 1
        else:
            num_of_categorical = len(self._tree_params.categorical_columns)
            num_of_numeric = len(self._tree_params.numeric_columns)
            density = (num_of_categorical + num_of_numeric) / (num_of_numeric + sum(categories_lengths))
        return density

    def _process_features(self, df, categories_lengths, sparse=True, categorical_features_suffix=False):
        """
        Combine the features in the input spark DataFrame into one column,
        either dense or sparse vector (depends on sparse parameter).
        Clean up all other columns containing features data.
        """
        def combine_features(numeric_values, categorical_values, category_lengths):
            num_len = len(numeric_values)
            indices = list(range(num_len))
            values = [float(x) for x in numeric_values]
            offset = num_len
            for cat_value, cat_length in zip(categorical_values, category_lengths):
                if 0 <= cat_value < cat_length:
                    indices.append(offset + cat_value)
                    values.append(1.0)
                offset += cat_length
            size = num_len + sum(category_lengths)
            vec = SparseVector(size, indices, values)
            if sparse:
                return vec
            else:
                return DenseVector(vec)

        combine_udf = f.udf(
            lambda *cols: combine_features(
                numeric_values=cols[:len(self._tree_params.numeric_columns)],
                categorical_values=cols[len(self._tree_params.numeric_columns):],
                category_lengths=categories_lengths
            ),
            VectorUDT()
        )
        suffix = '_index' if categorical_features_suffix else ''
        categorical_features = [f'{col}{suffix}' for col in self._tree_params.categorical_columns]
        # combine features to features column either sparse or dense
        df = df.withColumn(
            "features",
            combine_udf(*[f.col(col) for col in self._tree_params.numeric_columns + categorical_features])
        )

        # drop all old features columns (besides combined column with name "features")
        df = df.drop(*[col for col in df.columns
                       if col not in ['row_index_id', 'w', 'features', self._tree_params.target_column,
                                      self._tree_params.target_column + "_index",
                                      'level', 'chunk_index', self._tree_params.chunk_by, 'sensitivity']
                       ]
                     )
        return df

    def _process_ohe_features(self, df, spark_session):
        """
        Data preprocessing:
        - fill missing values same way as it's done on Tree Build
        - OHE for categorical features - using same categorical values as it's done for Coreset.
        Therefore, if input dataset contains new values, they will not produce new output features.
        - Target string-indexing, if target contains string data

        Output DataFrame contains "features" column, with preprocessed data.
        """
        transformers_list = []

        indexer = PersistStringIndexer(
            input_columns=self._tree_params.categorical_columns,
            output_column_suffix='_index',
            saved_category_path=self._tree_params.dhspark_path,
            spark=spark_session,
            allow_new_values=False
        )
        transformers_list.append(indexer)
        target_column = self._tree_params.target_column.replace('_index', '')
        if self._tree_params.target_column is not None and dict(df.dtypes)[target_column] == "string":
            y_indexer = PersistStringIndexer(
                input_columns=[target_column],
                output_column_suffix='_index',
                saved_category_path=self._tree_params.dhspark_path,
                spark=spark_session,
                allow_new_values=False
            )
            transformers_list.append(y_indexer)

        df = self._execute_pipline(df, transformers_list)

        numeric_assembler = VectorAssembler(
            inputCols=self._tree_params.numeric_columns,
            outputCol="numeric_features"
        )
        # one-hot encode categorical features
        ohe_encoders = [
            OneHotEncoder(inputCol=col, outputCol=f"{col}_ohe", dropLast=False)
            for col in [c + "_index" for c in self._tree_params.categorical_columns]
        ]
        # Combine OHE outputs with numeric features
        ohe_output_cols = [f"{col}_index_ohe" for col in self._tree_params.categorical_columns]
        final_assembler = VectorAssembler(inputCols=["numeric_features"] + ohe_output_cols, outputCol="features")
        # Create pipeline
        pipeline = Pipeline(stages=[numeric_assembler] + ohe_encoders + [final_assembler])
        # Fit and transform the data
        model = pipeline.fit(df)
        return model.transform(df)

    def _perform_string_indexing(self, df, spark_session):
        transformers_list = []

        indexer = PersistStringIndexer(
            input_columns=self._tree_params.categorical_columns,
            output_column_suffix='_index',
            saved_category_path=self._tree_params.dhspark_path,
            spark=spark_session,
            allow_new_values=False
        )
        transformers_list.append(indexer)
        target_column = self._tree_params.target_column.replace('_index', '')
        if self._tree_params.target_column is not None and dict(df.dtypes)[target_column] == "string":
            y_indexer = PersistStringIndexer(
                input_columns=[target_column],
                output_column_suffix='_index',
                saved_category_path=self._tree_params.dhspark_path,
                spark=spark_session,
                allow_new_values=False
            )
            transformers_list.append(y_indexer)

        return self._execute_pipline(df, transformers_list)

    def auto_preprocessing(
            self,
            spark_session: SparkSession,
            df,
            output_format: str = OutputFormat.SPARK_DF,
            sparse_threshold: float = 0.01,
    ) -> DataFrame:
        """
        On the base of input DataFrame returns data after OHE with same output features
        as Coreset Tree was built. If target has string type, string indexing will be applied to it.
        Parameters:
            spark_session: Spark session object
            df: input data as spark DataFrame
            output_format: output data format
                -spark_df - Returns data as spark DataFrame, `features` column has either DenseVector type
                    (when data density >= sparse_threshold) or SparseVector (density < sparse_threshold).
                    If there is a target, it's column name same as in original data.
                - matrix - return dict with fields 'X', 'y' where X either as numpy array, or csr_matrix.
                - pandas_df - return dict with fields 'X', 'y' where X is pandas DataFrame,
                    disregarding density of data and sparse_threshold value.
            sparse_threshold: based on data density and this value method returns data either in sparse or dense format.
        """
        df = self._handle_missing_values_params(df)
        df = self._perform_string_indexing(df, spark_session)
        categories_lengths = self._get_categories_lengths()
        return_sparse = self._get_density(categories_lengths) < sparse_threshold
        if output_format == OutputFormat.SPARK_DF:
            df = self._process_features(
                df=df,
                categories_lengths=categories_lengths,
                sparse=return_sparse,
                categorical_features_suffix=True
            )
            df = df.select(*["features", self._tree_params.target_column])
            return df
        else:
            # works for both PANDAS_DF and matrix (difference only for 'X' field - implemented before return)
            pandas_df = df.toPandas()
            numeric_data = pandas_df[self._tree_params.numeric_columns].to_numpy()
            cat_indexes = pandas_df[[col + '_index' for col in self._tree_params.categorical_columns]].to_numpy()
            sparse_matrix = _get_matrix(
                numerical_data=numeric_data,
                one_hot_indices=cat_indexes,
                cat_lengths=categories_lengths
            )
            features_names = self._get_output_features()
            if output_format == OutputFormat.MATRIX:
                result = {'X': sparse_matrix if return_sparse else sparse_matrix.toarray()}
            else:
                # PANDAS_DF
                result = {'X': pd.DataFrame(data=sparse_matrix.toarray(), columns=features_names)}

            if self._tree_params.target_column is not None:
                result['y'] = pandas_df[self._tree_params.target_column].to_numpy()
            return result

    def get_coreset(
            self,
            spark_session: SparkSession,
            level: int = 0,
            seq_from=None,
            seq_to=None,
            save_path=None,
            preprocessing_stage: str = PreprocessingStage.AUTO,
            output_format: str = OutputFormat.SPARK_DF,
            sparse_threshold: float = 0.01,
    ) -> DataFrame:
        """
        Get the coreset from the tree by tree path and return as spark.DataFrame
        with weights and sensitivities as additional columns of DataFrame
        Parameters:
            spark_session: Spark session object
            level: coreset level coreset level =0 for root, coreset level = 1 for level below the root, etc
            seq_from: Any, optional. The start of the time range from which to return the coreset.
            seq_to : Any, optional. The end of the time range from which to return the coreset.
            save_path: for saving the coreset outside the coreset tree
            preprocessing_stage:
                The different stages reflect the data preprocessing workflow.<br/><br/>
                - **user_no_missing_vals** - Return the data after any user defined data preprocessing (if defined)
                AND filling missing values.<br/><br/>
                - **user** - Return the data after any user defined data preprocessing (if defined).<br/><br/>
                - **auto** - Return the data after applying auto-preprocessing, including filling missing values,
                one-hot-encoding, converting Boolean fields to numeric, etc.
            sparse_threshold:
                Returns the features (X) as a sparse matrix if the data density after preprocessing is below
                sparse_threshold, otherwise, will return the data as an array
                (Applicable only for preprocessing_stage=`auto`).
            output_format: output data format
                -spark_df - return data as spark dataframe.
                    for preprocessing_stage in ['user_no_missing_vals', 'user']
                    returns original data  + [row_index_id, weights]
                    for preprocessing_stage = auto, returns data after processing (including OHE for
                    categorical features), in sparse or dense format (depends on density of data and sparse_threshold)
                - matrix - return data either as numpy array, or csr_matrix.
                    for preprocessing_stage in ['original', 'user'] returns original data  + [row_index_id, weights]
                    as dense numpy array
                    for preprocessing_stage = auto, returns data after processing (including OHE for
                    categorical features), as numpy array or csr_matrix (depends on density of data and sparse_threshold)
                - pandas_df - return original data as pandas dataframe,
                    disregarding both preprocessing_stage and sparse_threshold
        """
        assert preprocessing_stage in [PreprocessingStage.USER_NO_MISSING_VALUES,
                                       PreprocessingStage.AUTO,
                                       PreprocessingStage.USER
                                       ]
        # there are cases when we should raise an exception
        # - SaveOrig.NONE, only numeric features,  preprocessing_stage='user'
        # - SaveOrig.NONE, categorical features, preprocessing_stage = 'user'
        # - SaveOrig.NONE, categorical features, preprocessing_stage = 'user_no_missing_values'
        save_orig_error_message = ('In order to get original data one should set parameter save_orig = True '
                                   'on the service object initialization')
        if self._tree_params.save_orig == SaveOrig.NONE and preprocessing_stage == PreprocessingStage.USER:
            raise RuntimeError(save_orig_error_message)
        if (self._tree_params.save_orig == SaveOrig.NONE and self.has_categorical()
                and preprocessing_stage == PreprocessingStage.USER_NO_MISSING_VALUES):
            raise RuntimeError(save_orig_error_message)

        # loading the tree
        tree = self._load(dhspark_path=self._tree_params.dhspark_path, spark=spark_session)
        df_level = self._retrieve_coreset(level=level, tree=tree, spark=spark_session, seq_from=seq_from,
                                          seq_to=seq_to)

        df_level = self._split_and_process_df(df_level, preprocessing_stage, tree)

        if self._tree_params.trace_mode not in TRACE_MODE_VALUES:
            if output_format == OutputFormat.SPARK_DF:
                # we will need row_index_id for MATRIX and PANDAS options
                columns_to_remove = ["chunk_index", "level", "sensitivity", "row_index_id"]
                df_level = df_level.drop(*columns_to_remove)
            df_level = self._format_coreset_columns(coreset_df=df_level)

        if preprocessing_stage != PreprocessingStage.AUTO:
            if output_format == OutputFormat.SPARK_DF:
                if save_path is not None:
                    spark_session.sparkContext.setJobDescription("get_coreset - Save Coreset Data")
                    df_level.write.parquet(path=save_path, mode="overwrite")
                return df_level
            else:
                # the only difference here - either we return X as pandas df or as numpy array
                non_feature_columns = ['row_index_id', 'w']
                if self._tree_params.target_column is not None:
                    non_feature_columns += [self._tree_params.target_column.replace("_index", '')]
                select_columns = (self._tree_params.numeric_columns +
                                  self._tree_params.categorical_columns + non_feature_columns)
                pandas_df = df_level.select(select_columns).toPandas()

                if output_format == OutputFormat.PANDAS_DF:
                    if save_path is not None:
                        pandas_df.to_parquet(save_path)

                df_X = pandas_df[self._tree_params.numeric_columns +
                                 self._tree_params.categorical_columns]
                # fit both for OutputFormat.PANDAS_DF and OutputFormat.MATRIX
                result_dict = {
                    'ind': pandas_df['row_index_id'].to_numpy(),
                    'X': df_X if output_format == OutputFormat.PANDAS_DF else df_X.to_numpy(),
                    'w': pandas_df['w'].to_numpy(),
                }
                if self._tree_params.target_column is not None:
                    result_dict['y'] = pandas_df[self._tree_params.target_column.replace("_index", '')].to_numpy()
                return result_dict

        # from now on we are handling only preprocessing_stage == AUTO
        categories_lengths = self._get_categories_lengths()
        return_sparse = self._get_density(categories_lengths) < sparse_threshold

        if output_format == OutputFormat.SPARK_DF:
            df_level = self._process_features(df_level, categories_lengths, return_sparse)
            if save_path is not None:
                spark_session.sparkContext.setJobDescription("get_coreset - Save Coreset Data")
                df_level.write.parquet(path=save_path, mode="overwrite")
            return df_level
        else:
            # works for both PANDAS_DF and matrix (difference only for 'X' field - implemented before return)
            pandas_df = df_level.toPandas()
            numeric_data = pandas_df[self._tree_params.numeric_columns].to_numpy()
            cat_indexes = pandas_df[self._tree_params.categorical_columns].to_numpy()
            sparse_matrix = _get_matrix(
                numerical_data=numeric_data,
                one_hot_indices=cat_indexes,
                cat_lengths=categories_lengths
            )
            features_names = self._get_output_features()
            result = {
                'w': pandas_df['w'].to_numpy(),
                'features': features_names
            }
            if self._tree_params.target_column is not None:
                result['y'] = pandas_df[self._tree_params.target_column].to_numpy()
            if 'row_index_id' in pandas_df.columns:
                result['ind'] = pandas_df['row_index_id'].to_numpy()
            if output_format == OutputFormat.MATRIX:
                result['X'] = sparse_matrix if return_sparse else sparse_matrix.toarray()
            else:
                # PANDAS_DF
                result['X'] = pd.DataFrame(data=sparse_matrix.toarray(), columns=features_names)
            return result

    def has_categorical(self):
        return self._tree_params.categorical_columns is None or len(self._tree_params.categorical_columns) > 0

    def _decode_target(self, df):
        """
        Decoding target if ot was string-indexes, because original values was strings.
        We need it when calling get_coreset with preprocessing_stage <> AUTO
        """
        # target was not string-indexed at all
        if self._tree_params.target_column + '_index' in df.columns:
            return df
        full_categories_loaded = pd.read_parquet(
            os.path.join(self._tree_params.dhspark_path, 'string_indexer', 'all', 'categories.parquet')
        )
        # original target column name
        target_name = self._tree_params.target_column.replace('_index', '')
        # we do not have data for decoding
        if full_categories_loaded[full_categories_loaded['name'] == target_name].shape[0] == 0:
            return df

        # decoding itself
        target_values = full_categories_loaded[full_categories_loaded['name'] == target_name].iloc[0, 1]
        lookup_expr = f"array({', '.join([repr(v) for v in target_values])})"
        df = df.withColumn(target_name + '_index', f.col(target_name + '_index').cast("int"))
        df = df.withColumn(target_name, f.expr(f"{lookup_expr}[{target_name + '_index'} - 1]"))
        # remove string-indexed values
        df = df.drop(target_name + '_index')
        return df

    def _split_features(self, df, include_features=False):
        # splitting only numeric columns from features column  to the original columns names
        original_cols = df.columns
        if not include_features:
            original_cols = [col_name for col_name in df.columns if col_name != "features"]
        # Use selectExpr to split the array into individual columns
        split_cols = [f.expr(f"features[{idx}] as {col}")
                      for idx, col in
                      enumerate(self._tree_params.numeric_columns + self._tree_params.categorical_columns)
                      ]
        # Select the id column and the new split columns
        select = df.select(*original_cols, *split_cols)

        return select

    def _format_coreset_columns(self, coreset_df: DataFrame):
        if self._tree_params.chunk_by is not None and self._tree_params.chunk_size is not None:
            # Remove the '_sc_' suffix and any numbers following it
            coreset_df = coreset_df.withColumn(self._tree_params.chunk_by,
                                               f.regexp_replace(self._tree_params.chunk_by, f"{SUB_CHUNK_PREFIX}\\d+",
                                                                ""))
            # Convert the cleaned string to a proper date format
            coreset_df = coreset_df.withColumn(
                self._tree_params.chunk_by,
                f.to_date(
                    self._tree_params.chunk_by,
                    convert_pandas_date_format_to_spark_date_format(
                        self._tree_params.data_params.seq_column.get("datetime_format"))
                )
            )

        return coreset_df

    def _retrieve_coreset(self, level, seq_from, seq_to, tree: TreeDataFrame, spark):
        # regular_level=0 for root, regular_level=1 for level below the root, etc
        tree_params = self._tree_params
        coreset_df = None
        if seq_to is not None and seq_from is not None and tree_params.chunk_by_tree is not None:
            # handle seq column here if exits add index column here since there is no index in chunk by date
            pd_match_df = self._find_closest_match_chunks(tree_metadata=tree_params.chunk_by_tree, seq_from=seq_from,
                                                          seq_to=seq_to)
            if pd_match_df is not None and not pd_match_df.empty:
                for _, row in pd_match_df.iterrows():
                    print(f"The row to use to get the coreset {row}")
                    df = tree.getLevelDF(row["level"])
                    df = df.where(f.col('chunk_index') == row["chunk_index"])
                    if coreset_df is None:
                        coreset_df = df
                    else:
                        coreset_df = coreset_df.union(df)

                if coreset_df is None:
                    return coreset_df

        else:
            regular_level = tree.getTreeSize() - level - 1

            print(f"retrieve coreset the tree level to get is : {regular_level}")
            coreset_df = tree.getLevelDF(regular_level)

            # add orphan heads
            orphan_heads = self._get_orphan_for_level(
                n_leaves=tree_params.first_level_max_chunk,
                level=regular_level,
                leaf_factor=tree_params.leaf_factor
            )
            for single_orphan_head in orphan_heads:
                level_index = single_orphan_head[0]
                node_index = single_orphan_head[1] + 1
                df_node = tree.getLevel(level_index).level_df.where(f.col('chunk_index') == node_index)
                coreset_df = coreset_df.union(df_node)

        return coreset_df

    def _create_chunk_by_pandas_tree(self, pd_df, chunk_by):
        # crating the group by chunks and first level coreset size floor the coreset size.

        chunk_by_tree = self._create_chunk_by_metadata_tree(pd_df, self._tree_params.data_params.seq_column.get(
            "datetime_format"), chunk_by)
        max_chunk = len(chunk_by_tree[0])
        self._tree_params.chunk_by_tree = chunk_by_tree
        return max_chunk

    def _create_chunk_by_metadata_tree(self, pdf: pd.DataFrame, date_format, chunk_by):
        """
        Function to create a hierarchical tree structure by summing adjacent chunks.
        This creates multiple levels of aggregation, starting from the base chunked data
        and progressively averaging adjacent rows, resulting in a tree structure.

        Args:
            pdf (pd.DataFrame): Input dataframe this is the group by spark result in pandas data frame ordered by seq
            date_format (str): Optional string to parse date columns if needed.
            chunk_by (str): The column to group the data by.

        Returns:
            list: A list of dataframes representing different levels of the tree.
        """

        # Tree-related parameters, typically coming from class-level variables
        tree_params = self._tree_params
        levels = []  # List to hold the hierarchical levels
        start_seq = []  # List to store the start sequences of chunks

        level_num = 0  # Initialize the level number for the tree

        # Process each row to extract or format the 'chunk_by' value
        for i in range(0, len(pdf)):
            chunk_by_value = pdf.iloc[i][chunk_by]

            # If the value is a string and a date format is provided, convert to datetime
            if isinstance(chunk_by_value, str) and date_format is not None:
                chunk_by_value = chunk_by_value.split(SUB_CHUNK_PREFIX)[0]
                chunk_by_value = datetime.strptime(chunk_by_value, date_format)

            start_seq.append(chunk_by_value)  # Append the processed value to start_seq

        # Assign an incremental index starting from 1 to each chunk
        pdf['chunk_index'] = pdf.index + 1

        # Add new columns to the dataframe for start, end sequences and level number
        pdf = pdf.assign(start_seq=start_seq)
        pdf = pdf.assign(end_seq=start_seq)
        pdf = pdf.assign(level=[level_num] * len(pdf))  # Assign level 0 to all chunks

        # Drop the original chunk_by column as it's no longer needed
        pdf = pdf.drop(chunk_by, axis=1)

        # Handle cases where we are partially building the tree (concatenating with old data) used the partal build
        if tree_params.partial_build_ending_chunk_by is not None and tree_params.chunk_by_tree is not None:
            old_df = tree_params.chunk_by_tree[0]
            pdf['chunk_index'] = pdf.index + len(old_df) + 1  # Adjust chunk index to account for old data
            # Concatenate the old dataframe with the new one
            pdf = pd.concat([old_df, pdf])

        levels.insert(0, pdf)  # Insert the base level of the tree
        current_df = pdf.copy()  # Make a copy of the current level dataframe

        # Iteratively create higher levels by averaging adjacent chunks
        while len(current_df) > 1:
            level_num += 1  # Increment the level number
            next_level_averages = []  # List to store coreset size averages
            start_seq = []  # List for the start sequence of the next level
            end_seq = []  # List for the end sequence of the next level

            # Iterate over the current dataframe in steps of 2 to sum adjacent rows
            for i in range(0, len(current_df), 2):
                if i + 1 < len(current_df):
                    # Average the coreset sizes of two adjacent rows
                    average_count = (current_df.iloc[i]['coreset_size'] + current_df.iloc[i + 1]['coreset_size']) / 2
                    start_seq.append(current_df.iloc[i]["start_seq"])  # Use start_seq of the first row
                    end_seq.append(current_df.iloc[i + 1]["end_seq"])  # Use end_seq of the second row
                    next_level_averages.append(average_count)  # Append the average coreset size

            # Create a new DataFrame for the next level
            next_level_df = pd.DataFrame({
                'coreset_size': next_level_averages,
                'chunk_index': range(1, len(next_level_averages) + 1),  # Assign chunk indices
                'start_seq': start_seq,
                'end_seq': end_seq,
                'level': [level_num] * len(next_level_averages)  # Assign the current level number
            })

            # Append the new level to the levels list and update current_df
            levels.append(next_level_df)
            current_df = next_level_df.copy()

        return levels  # Return the list of dataframes representing each level of the tree

    def _check_in_range(self, date_to_search, chunk_start, chunk_end, level_matched_chunks):
        # Function to find the closest match for the date range with preference for lower levels if they fit better
        for date_range in date_to_search:
            if chunk_start >= date_range[0] and chunk_end <= date_range[1]:
                return True
        # if in the level there is another chunk with the same date which is a match after finding the first one
        # in case of chunk size is spacafied
        for row in level_matched_chunks:
            if chunk_start == row["start_seq"] and chunk_end == row["end_seq"]:
                return True

        return False

    def _update_seq_range(self, seq_to_search, chunk_start, chunk_end, time_diff):
        # Function to update the date rage only date ranges which fit the rage are updated and
        # this function will add new ranges to look for and remove the old one until the maximum range is covered.
        dates_to_add = set()
        dates_to_remove = set()

        for seq_range in seq_to_search:
            # checking again if dates in range
            if chunk_start >= seq_range[0] and chunk_end <= seq_range[1]:
                remove_date_range = False
                start_diff = chunk_start - seq_range[0]
                start_diff_sec = int(start_diff.total_seconds())
                # if we have new ranges to add in the beginning of the date range
                if start_diff_sec > 0:
                    remove_date_range = True
                    dates_to_add.add((seq_range[0], chunk_start - time_diff))
                end_diff = seq_range[1] - chunk_end
                end_diff_sec = int(end_diff.total_seconds())
                # if we have new ranges to add in the end of the date range
                if end_diff_sec > 0:
                    remove_date_range = True
                    dates_to_add.add((chunk_end + time_diff, seq_range[1]))
                # if no new ranges are needed we have the range we only remove.
                if end_diff_sec == 0 and start_diff_sec == 0:
                    remove_date_range = True
                if remove_date_range:
                    dates_to_remove.add(seq_range)
        seq_to_search.difference_update(dates_to_remove)
        seq_to_search.update(dates_to_add)
        return seq_to_search

    def _find_closest_match_chunks(self, tree_metadata, seq_from, seq_to):
        """
        Finds the closest matching chunks for a specified date range in a tree structure.
        The function will try to complete the coreset range.
        We are traversing the tree from the highest level to the lowest and on each leve we will try to find part
         or all the rang
        reducing the range each time we find a match
        we are also  checking the previous or next coreset of the matched coresets to see if we need to complete
        the creset this is done
        until we finsh traversing the tree or finished finding the coresets that match the range
        and finishing completing those coresets with
        leftover coresets.
        For Example (only relevant tree data is displayed),
        we want to find  coreset range 2023-06-14-2023-06-16
        Level 5 data:
        chunk_index  start_seq  end_seq    level
        ....
        73	         2023-06-10	2023-06-12	5
        74	         2023-06-12	2023-06-14	5
        75	         2023-06-14	2023-06-16	5
        76	         2023-06-17	2023-06-18	5
        77	         2023-06-18	2023-06-21	5
        ....

        So here we see that we find the match on level 5 of the tree chunk_index 75
        (this is  handled in matched_chunks array and _update_seq_range func)

        but from looking at the next chunk 76 we see that we are out of range and from looking at previous chunk_index
        chunk_index 74 we see that part of day 2023-06-14 is in this coreset as well
        (this is done by adding the chunk to coreset_to_search dic using _add_not_complete_coreset_chunk )
        so we need to continue moving down the tree
        levels to complete this coreset  now we are checking only this range 2023-06-14

        chunk_index  start_seq   end_seq     level
        ....
        146	         2023-06-11	2023-06-12   4
        147	         2023-06-12	2023-06-13   4
        148	         2023-06-14	2023-06-14   4
        149	         2023-06-14	2023-06-15   4
        150	         2023-06-16	2023-06-16   4
        ....
       so when we get to level 4 of the tree we can see that we can complete the missing day with chunk_index 148 and
        from checking
       the previous and next chunk of this coreset (147,149) we see that no days need to be completed
       (this is done partly by calculating
       for all matching coresets what they are comprised from in the current level
       in _calculate_all_level_chunk_for_coreset func)  and the range is done.

       :param tree_metadata: A list of DataFrames, where each DataFrame represents a tree level containing
       chunk metadata.
       :param seq_from: The start of the date range to match, as a string or datetime.
       :param seq_to: The end of the date range to match, as a string or datetime.
       :return: A DataFrame containing the matched chunks or an empty DataFrame if no match is found.
        """
        # Convert input dates to datetime objects
        date_range_start = pd.to_datetime(seq_from)
        date_range_end = pd.to_datetime(seq_to)

        matched_chunks = []  # Stores matched chunks
        size_coreset_levels_arr = []  # Tracks the size of each level
        date_to_search = set()  # A set of tuples representing date ranges to match
        coreset_to_search = dict()  # Tracks coresets to search in subsequent iterations

        # Initialize with the input date range
        date_to_search.add((date_range_start, date_range_end))

        # Calculate the time difference granularity for sequence column
        time_diff = self._calculate_time_diff_granularity(self._tree_params.data_params.seq_column.get("granularity"))

        # Iterate through the tree levels in reverse order (from top level to bottom level)
        tree_size = len(tree_metadata)
        for level_df in reversed(tree_metadata):
            level_match = []  # Stores matches for the current level
            size_coreset_levels_arr.append(len(level_df))  # Add the current level size
            coreset_to_search_add = dict()  # Tracks new coresets to search
            coreset_to_search_remove = set()  # Tracks coresets to remove

            for i, chunk_tuple in enumerate(level_df.iterrows()):
                # Get start and end sequences for the chunk
                chunk = chunk_tuple[1]
                chunk_start = chunk['start_seq']
                chunk_end = chunk['end_seq']

                # Fetch the previous and next chunks if available
                next_chunk = level_df.iloc[i + 1] if i + 1 <= size_coreset_levels_arr[-1] - 1 else None
                prev_chunk = level_df.iloc[i - 1] if i - 1 > 0 else None

                # Check if the chunk is within the search range
                if self._check_in_range(date_to_search, chunk_start, chunk_end, level_match):
                    matched_chunks.append(chunk)  # Add to matched chunks
                    level_match.append(chunk)  # Add to the current level match

                    # Add chunk to coreset search and check previous and next chunk to complete the coreset
                    coreset_to_search = self._add_not_complete_coreset_chunk(coreset_to_search, chunk, prev_chunk,
                                                                             next_chunk)
                    # update the search range
                    date_to_search = self._update_seq_range(
                        seq_to_search=date_to_search, chunk_start=chunk_start, chunk_end=chunk_end, time_diff=time_diff
                    )

                # Check for matching coresets across levels if we need to complete the coreset
                all_chunk_indexes = set()
                for coreset_key, coreset_item in coreset_to_search.items():
                    if (  # checking only matches in lower levels then the coreset to search.
                            coreset_item[0]["level"] > chunk["level"]
                            and chunk["end_seq"] == coreset_item[1]
                            and chunk["start_seq"] == coreset_item[1]
                    ):
                        # Getting all children coresets for all matched coreset for current level
                        for match_chunk in matched_chunks:
                            coreset_chunk_indexes = self._calculate_all_level_chunk_for_coreset(
                                coreset=match_chunk,
                                size_coreset_levels_arr=size_coreset_levels_arr,
                                tree_size=tree_size,
                                level_df=level_df
                            )
                            all_chunk_indexes.update(coreset_chunk_indexes)

                        # Add current chunk if not already included to complete the coreset
                        if chunk["chunk_index"] not in all_chunk_indexes:
                            matched_chunks.append(chunk)
                            coreset_to_search_remove.add(coreset_key)
                            # check if previous and next chunks are not already in the coreset
                            if prev_chunk is not None and prev_chunk["chunk_index"] in all_chunk_indexes:
                                prev_chunk = None
                            if next_chunk is not None and next_chunk["chunk_index"] in all_chunk_indexes:
                                next_chunk = None
                            # Add chunk to coreset search and check previous and next chunk to complete the coreset
                            coreset_to_search_add = self._add_not_complete_coreset_chunk(
                                coreset_to_search=coreset_to_search_add,
                                chunk=chunk,
                                prev_chunk=prev_chunk,
                                next_chunk=next_chunk
                            )

            # Update coresets to search, removing and adding as necessary(updating range)
            for remove_key in coreset_to_search_remove:
                del coreset_to_search[remove_key]
            coreset_to_search.update(coreset_to_search_add)

            # Break if there are no more ranges or coresets to search
            if len(date_to_search) == 0 and len(coreset_to_search) == 0:
                break
        print(f"The total number of match chunks found {len(matched_chunks)}")
        # Return matched chunks if any, else an empty DataFrame
        return pd.DataFrame(matched_chunks) if matched_chunks else pd.DataFrame()

    def _calculate_time_diff_granularity(self, granularity):
        if granularity == "D":
            return timedelta(days=1)
        elif granularity == "H":
            return timedelta(hours=1)
        elif granularity == "M":
            return timedelta(minutes=1)
        elif granularity == "S":
            return timedelta(seconds=1)
        elif granularity == "W":
            return timedelta(weeks=1)

    def _add_not_complete_coreset_chunk(self, coreset_to_search, chunk, prev_chunk, next_chunk):
        """
        Add not completed coreset chunks to the search dictionary to find matching coreset in lower levels.
        if a previous or next coreset holds part of the seq of the match coreset found.
        This dictinary key :level,chunk_index,seq_to_find (end seq or start seq)
        The value: is the chunk object and the seq to find (end seq or start seq).
        Depending on which coreset needs to be completed the previous or next or both.

        :param coreset_to_search: Dictionary of coresets to search.
        :param chunk: Current chunk.
        :param prev_chunk: Previous chunk.
        :param next_chunk: Next chunk.
        :return: Updated dictionary of coresets to search.
        """
        # Add the current chunk if it is connected to the previous chunk
        if prev_chunk is not None and prev_chunk["end_seq"] == chunk["start_seq"]:
            coreset_to_search[(chunk["level"], chunk["chunk_index"], chunk["start_seq"])] = (chunk, chunk["start_seq"])
        # Add the current chunk if it is connected to the next chunk
        if next_chunk is not None and next_chunk["start_seq"] == chunk["end_seq"]:
            coreset_to_search[(chunk["level"], chunk["chunk_index"], chunk["end_seq"])] = (chunk, chunk["end_seq"])

        return coreset_to_search

    def _calculate_all_level_chunk_for_coreset(self, coreset, size_coreset_levels_arr, tree_size, level_df):
        """
        Calculate all chunks across levels for a given coreset(chunk_index) .
        For  example: a coreset on level 5
       chunk_index   start_seq   end_seq     level
         75	         2023-06-14	2023-06-16	5

        I would like to find what are the matching coreset for this one on level 4:
        chunk_index   start_seq   end_seq     level
        149	          2023-06-14	 2023-06-15	4
        150	          2023-06-16	 2023-06-16	4
        This function calculate fore each match coreset on level X what coresets represent it on  lower levels level X -y

        :param coreset: The coreset chunk to evaluate.
        :param size_coreset_levels_arr: Array of level sizes.
        :param tree_size: Total number of tree levels.
        :param level_df: DataFrame representing the current level.
        :return: Set of all chunk indexes corresponding to the coreset.
        """
        # Determine the level index of the coreset
        level_index = tree_size - coreset["level"] - 1

        # Calculate the ratio of the current level size to the coreset level size
        coreset_level_ratio = size_coreset_levels_arr[-1] // size_coreset_levels_arr[level_index]

        # Determine the start and end range for the coreset
        chunk_index_to_search = coreset["chunk_index"]
        start_index = int((chunk_index_to_search - 1) * coreset_level_ratio) + 1
        end_index = int(chunk_index_to_search * coreset_level_ratio)

        # check all matching chunks in range
        level_coreset_indexes = set()
        for i in range(start_index, end_index + 1):
            if coreset["start_seq"] <= level_df.iloc[i - 1]["start_seq"] and coreset["end_seq"] >= level_df.iloc[i - 1][
                "end_seq"]:
                level_coreset_indexes.add(i)
        return level_coreset_indexes

    def _set_trace_mode(self, spark_session: SparkSession):
        trace_mode_value = spark_session.conf.get(DHSPARK_TRACE_MODE_CONF, None)
        if trace_mode_value is not None:
            self._tree_params.trace_mode = trace_mode_value.lower()

    def _set_chunk_sample_ratio(self):
        chunk_sample_ratio = self._tree_params.chunk_sample_ratio
        if chunk_sample_ratio is None:
            if self._tree_params.n_instances is not None:
                row_number_factor = 1_000_000
                if self._tree_params.n_instances <= row_number_factor:
                    chunk_sample_ratio = 1.0
                elif row_number_factor < self._tree_params.n_instances <= 10 * row_number_factor:
                    chunk_sample_ratio = 0.2
                elif 10 * row_number_factor < self._tree_params.n_instances <= 100 * row_number_factor:
                    chunk_sample_ratio = 0.1
                elif 100 * row_number_factor < self._tree_params.n_instances <= 1000 * row_number_factor:
                    chunk_sample_ratio = 0.05
                else:
                    chunk_sample_ratio = 0.01
            else:
                chunk_sample_ratio = 0.05

        self._tree_params.chunk_sample_ratio = chunk_sample_ratio
