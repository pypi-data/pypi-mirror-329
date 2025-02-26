import pytest

from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    spark = (SparkSession.builder.master("local[*]")
             .appName("Testing PySpark Session").
             config("spark.driver.bindAddress", "localhost").
             config("spark.ui.port", "4050").
             config("spark.sql.shuffle.partitions", 1).
             # config("spark.sql.parquet.compression.codec", "zstd").
             config("spark.sql.execution.arrow.pyspark.enabled", "true").
             config("spark.sql.execution.pythonUDF.arrow.enabled", "true").
             config("spark.sql.execution.pythonUDTF.arrow.enabled", "true").
             # config("spark.hadoop.fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem").
             # config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2").
             # config("spark.sql.parquet.enableVectorizedReader","false").
             # config("spark.sql.shuffle.partitions", 1).
             # config("spark.sql.sources.partitionOverwriteMode", "dynamic").
             #          config("spark.sql.parquet.output.committer.class", "org.apache.parquet.hadoop.ParquetOutputCommitter").
             # config("spark.sql.sources.commitProtocolClass",
             #                "org.apache.spark.sql.execution.datasources.SQLHadoopMapReduceCommitProtocol").

             getOrCreate())
    yield spark

    spark.stop()
