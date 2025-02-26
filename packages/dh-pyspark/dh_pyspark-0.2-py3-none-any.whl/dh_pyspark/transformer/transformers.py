import os

import numpy as np
import pandas as pd
import pyspark.ml.functions as mf
from pyspark.ml import Transformer
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.ml.param.shared import (
    HasInputCol,
    HasOutputCol,
    Param,
    Params,
    TypeConverters
)
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *


class PersistStringIndexerParams(HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    savedCategoryPath = Param(
        Params._dummy(),  # parent of the param, it is required to set to this placeholder
        "savedCategoryPath",  # name of the param
        "The path used to save the updated category data frame",  # desc of the param
        TypeConverters.toString
    )
    maxCategorySize = Param(
        Params._dummy(),  # parent of the param, it is required to set to this placeholder
        "maxCategorySize",  # name of the param
        "The maximum number of categories to save categories will be ordered by count.",  # desc of the param
        TypeConverters.toInt  # try to convert param to a list of strings
    )

    def __init__(self):
        super().__init__()
        # good practice: set default values for params
        self._setDefault(savedCategoryPath=None)
        self._setDefault(maxCategorySize=None)

        # getter and setter for keepValues

    def getSavedCategoryPath(self):
        return self.getOrDefault(self.savedCategoryPath)

    def setSavedCategoryPath(self, path):
        return self._set(savedCategoryPath=path)

    def getMaxCategorySize(self):
        return self.getOrDefault(self.maxCategorySize)

    def setMaxCategorySize(self, maxCategorySize):
        return self._set(maxCategorySize=maxCategorySize)


class PersistStringIndexer(Transformer, PersistStringIndexerParams):
    """
    A PySpark Transformer to add an index to a categorical data column based on a model fitted by CategoricalFreqencyIndexer.
    """

    def __init__(self, input_columns: list, output_column_suffix: str, saved_category_path: str = None,
                 spark: SparkSession = None, max_category_size: int = 100,
                 allow_new_values: bool = True):
        super(PersistStringIndexer, self).__init__()
        self.max_category_size = max_category_size
        self.input_columns = input_columns
        self.output_column_suffix = output_column_suffix
        self.saved_category_path = saved_category_path
        self.allow_new_values = allow_new_values
        # this is not a parameter since it is not serializable
        self.spark = spark
        self.max_map = {}

    def _transform(self, dataset: DataFrame) -> DataFrame:
        df_all = dataset
        saved_path = os.path.join(self.saved_category_path, '', 'string_indexer', 'all')
        saved_categories_exists = saved_path is not None and self.spark is not None and self.path_exists(saved_path)
        if saved_categories_exists:
            full_categories_loaded = pd.read_parquet(saved_path)
        else:
            full_categories_loaded = pd.DataFrame(columns=['name', 'values'])
        for column_idx, input_col in enumerate(self.input_columns):
            output_col = input_col + self.output_column_suffix
            if (full_categories_loaded['name'] == input_col).any():
                old_categories = full_categories_loaded[full_categories_loaded['name'] == input_col]
                old_categories = list(old_categories.iloc[0, 1])
            else:
                old_categories = []
            df = dataset.select(input_col)
            if self.allow_new_values:
                new_categories_df = (df.groupBy(input_col)
                                     .agg(f.count(input_col).alias("count"), )
                                     .orderBy('count', ascending=[False]))
                new_categories_df = new_categories_df.limit(self.max_category_size).select(input_col)
                # new_categories as list on driver
                new_categories = [r[input_col] for r in new_categories_df.collect()]
                # remove values that we meet before
                new_categories = list(set(new_categories) - set(old_categories))
                # union values that we meet before with new ones
                full_categories = old_categories + new_categories
            else:
                full_categories = old_categories

            @f.pandas_udf(IntegerType())
            def udf_create_index_by_column(column: pd.Series) -> pd.Series:
                index_map = {value: idx + 1 for idx, value in enumerate(full_categories)}
                return pd.Series(column.map(index_map).fillna(0).astype(int))

            df_all = df_all.withColumn(output_col, udf_create_index_by_column(f.col(input_col)))
            if (full_categories_loaded['name'] == input_col).any():
                full_categories_loaded.loc[full_categories_loaded['name'] == input_col, 'values'] = [full_categories]
            else:
                new_row = pd.DataFrame({'name': input_col, 'values': [full_categories]})
                full_categories_loaded = pd.concat([full_categories_loaded, new_row], ignore_index=True)
        if self.allow_new_values:
            # save categorical values
            os.makedirs(saved_path, exist_ok=True)
            full_categories_loaded.to_parquet(os.path.join(saved_path, 'categories.parquet'))
        return df_all

    def path_exists(self, path):
        sc = self.spark.sparkContext
        hpath = sc._jvm.org.apache.hadoop.fs.Path(path)
        fs = hpath.getFileSystem(sc._jsc.hadoopConfiguration())
        return (not fs.globStatus(hpath) is None) and (len(fs.globStatus(hpath)) > 0)


class PedNotEqualParams(HasInputCol, HasOutputCol, DefaultParamsReadable, DefaultParamsWritable):
    maxSize = Param(
        Params._dummy(),  # parent of the param, it is required to set to this placeholder
        "maxSize",  # name of the param
        "the max size to ped to en existing vector or array",  # desc of the param
        TypeConverters.toInt
    )
    isVector = Param(
        Params._dummy(),  # parent of the param, it is required to set to this placeholder
        "isVector",  # name of the param
        "the transformer list type vector true array false",  # desc of the param
        TypeConverters.toBoolean
    )

    def __init__(self):
        super().__init__()
        # good practice: set default values for params
        self._setDefault(maxSize=None, isVector=False)

    def getMaxSize(self):
        return self.getOrDefault(self.maxSize)

    def setMaxSize(self, maxSize):
        return self._set(maxVectorSize=maxSize)

    def getIsVector(self):
        return self.getOrDefault(self.isVector)

    def setIsVector(self, isVector):
        return self._set(isVector=isVector)


class PedNotEqual(Transformer, PedNotEqualParams):
    def __init__(self, input_column: str, output_column: str, max_array_size: int = None):

        super(PedNotEqual, self).__init__()
        self._setDefault(inputCol=input_column, outputCol=output_column, maxSize=max_array_size)

    def _transform(self, dataset: DataFrame) -> DataFrame:
        input_col = self.getInputCol()
        output_col = self.getOutputCol()
        max_size = self.getMaxSize()
        return_type = dataset.schema[input_col].dataType
        is_vector = return_type == VectorUDT()
        if max_size is None:
            if is_vector:
                max_size = dataset.agg(f.max(f.size(mf.vector_to_array(f.col(input_col))))).collect()[0][0]
            else:
                max_size = dataset.agg(f.max(f.size(f.col(input_col)))).collect()[0][0]

        def resize_zero_vector(value, max_size: int, is_vector: bool):
            raw = value
            if is_vector:
                raw = value.toArray()

            arr_size = len(raw)
            dif_size = max_size - arr_size
            if dif_size > 0:
                raw = np.append(raw, [0] * dif_size).tolist()
            if is_vector:
                return Vectors.dense(raw)

            return raw

        resize_zero_vector_udf = f.udf(
            lambda value: resize_zero_vector(value=value, max_size=max_size, is_vector=is_vector), return_type)
        return dataset.withColumn(output_col, resize_zero_vector_udf(f.col(input_col)))
