from dataclasses import dataclass

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession


@dataclass
class DHSparkSessionManager:
    spark: SparkSession = None  # SparkSession object
    spark_config: SparkConf = SparkConf()  # SparkConf object for configuration
    app_name: str = None  # Application name

    def create_session_config(self, app_name: str, spark_overrides: list = None):
        """
        Create Spark session configuration.

        Parameters:
            app_name (str): The name of the Spark application.
            spark_overrides (list): A list of Spark configuration overrides.
        """
        # Default Spark configurations
        spark_configs = {
            # "spark.hadoop.fs.s3.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            # "spark.sql.execution.arrow.pyspark.enabled": "true",
            # "spark.sql.execution.pythonUDF.arrow.enabled": "true",
            # "spark.sql.execution.pythonUDTF.arrow.enabled": "true",
        }
        # Add additional configurations if running in local mode
        # if is_local:
        #     spark_configs["spark.jars.packages"] = "org.apache.hadoop:hadoop-aws:3.3.2"
        # Add user-defined configurations if provided
        if spark_overrides is not None:
            spark_configs.update(spark_overrides)

        # Set Spark configurations
        self.spark_config.setAll(spark_configs.items())

        # Set the application name
        self.app_name = app_name

    def create_session(self):
        """
        Create a Spark session.

        Returns:
            SparkSession: The created Spark session.
        """
        # Create Spark context with specified configurations
        context = SparkContext(conf=self.spark_config)
        # Create Spark session using the Spark context
        self.spark = (SparkSession(context)
                      .builder
                      .appName(self.app_name)
                      .getOrCreate())

        return self.spark

    def stop_session(self):
        """
        Stop the Spark session.
        """
        # Check if Spark session exists
        if self.spark:
            # Stop Spark session
            self.spark.stop()


class DHSparkSession:
    session_manager: DHSparkSessionManager

    def __init__(self,
                 app_name: str,
                 spark_overrides: list = None,

                 ):
        """
        Initialize DHSparkSession.

        Parameters:
            app_name (str): The name of the Spark application.
            spark_overrides (list): A list of Spark configuration overrides.

        """
        # Create an instance of DHSparkSessionManager
        self.session_manager = DHSparkSessionManager()
        # Create Spark session configuration
        self.session_manager.create_session_config(app_name=app_name, spark_overrides=spark_overrides)

    def __enter__(self):
        """
        Define behavior for entering 'with' statement.
        """
        # Create and return Spark session
        return self.session_manager.create_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Define behavior for exiting 'with' statement.
        """
        # Stop Spark session
        self.session_manager.stop_session()
