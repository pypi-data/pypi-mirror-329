import datetime
import importlib
import logging
import os
import random
from calendar import monthrange

import pyspark.ml.functions as mf
import pyspark.sql.functions as f
from pyspark.ml.linalg import VectorUDT
from pyspark.sql import DataFrame
from pyspark.sql.types import ArrayType, DoubleType, IntegerType

logger = logging.getLogger(__name__)


def df_vector_to_array(df):
    for field in df.schema.fields:
        if field.dataType == VectorUDT():
            df = df.withColumn(field.name, mf.vector_to_array(field.name))
    return df


def df_array_to_vector(df: DataFrame):
    for field in df.schema.fields:

        if isinstance(field.dataType, ArrayType) and isinstance(field.dataType.elementType, DoubleType):
            df = df.withColumn(field.name, mf.array_to_vector(field.name))
    return df


def set_udf_logging(test: bool, filename: str = None):
    if test:  # this should not be used on EMR
        log_directory = os.path.dirname(filename)
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(filename=filename, encoding='utf-8', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-2s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filemode="a")


def convert_spark_date_format_to_pandas_date_format(spark_date_format: str) -> str:
    """
    Converts a PySpark date format to a pandas-compatible strftime format.

    Args:
        spark_date_format (str): PySpark date format string.

    Returns:
        str: Pandas-compatible date format string.
    """
    replacements = {
        'yyyy': '%Y',
        'yy': '%y',
        'MM': '%m',
        'dd': '%d',
        'HH': '%H',
        'hh': '%I',
        'mm': '%M',
        'ss': '%S'
    }

    pandas_format = spark_date_format
    for spark_token, pandas_token in replacements.items():
        pandas_format = pandas_format.replace(spark_token, pandas_token)

    return pandas_format


def convert_pandas_date_format_to_spark_date_format(pandas_date_format: str) -> str:
    """
    Converts a pandas-compatible strftime date format to a PySpark date format.

    Args:
        pandas_date_format (str): Pandas strftime date format string.

    Returns:
        str: PySpark-compatible date format string.
    """
    replacements = {
        '%Y': 'yyyy',
        '%y': 'yy',
        '%m': 'MM',
        '%d': 'dd',
        '%H': 'HH',
        '%I': 'hh',
        '%M': 'mm',
        '%S': 'ss'
    }

    spark_format = pandas_date_format
    for pandas_token, spark_token in replacements.items():
        spark_format = spark_format.replace(pandas_token, spark_token)

    return spark_format


def create_data(row, f, cf_arr, row_pare_date, starting_date):
    def generate_tuple(f, cf_arr, date_value, row_pare_date):
        random_string = ''.join(random.choice(['A', 'B']))  # Generate a random string A or B
        if cf_arr is None:
            row = [random_string] + [random.randint(1, 100) for _ in
                                     range(f)]
        else:
            row = [random_string] + [''.join(random.choice(cf)) for cf in cf_arr] + [random.randint(1, 100) for _ in
                                                                                     range(f)]
        if row_pare_date > 0:
            row = [date_value] + row
        return row

    data_rows = []
    date_val = starting_date
    for i in range(row):
        data_rows.append(generate_tuple(f, cf_arr, date_val, row_pare_date))
        if row_pare_date > 0 and i % row_pare_date == 0:
            date_val = date_val + datetime.timedelta(days=1)
    return data_rows


def create_data_frame(number_features, categorical_features_arr, number_rows, spark, missing_values=False,
                      row_pare_date=0, starting_date=datetime.datetime.now()):
    data = create_data(number_rows, number_features, categorical_features_arr, row_pare_date, starting_date)
    if missing_values:
        for i in range(len(data)):
            if i % 3 == 0:
                max_indx = len(data[i]) - 1
                s_index = 1
                if row_pare_date > 0:
                    s_index = 2
                indx = random.randint(s_index, max_indx)
                data[i][indx] = None
                if indx < max_indx and i % 6 == 0:
                    data[i][max_indx] = None

    f_arr = []
    len_cfa = 0
    if categorical_features_arr is not None:
        len_cfa = len(categorical_features_arr)

    for i in range(number_features + len_cfa):
        if i < len_cfa:
            col = f"f{i} string"
        else:
            col = f"f{i} int"

        f_arr.append(col)
    cols = ["y string"] + f_arr
    if row_pare_date > 0:
        cols = ["date date"] + cols

    rdd = spark.sparkContext.parallelize(data, 100)
    rdd = rdd.repartition(int(spark.conf.get('spark.sql.shuffle.partitions')))
    print(f"the new data size :  {rdd.count()}")
    df = rdd.toDF(",".join(cols))

    return df, f_arr


def create_random_dataframe_start_end_date(start_date: str, end_date: str, num_columns: int, spark, num_rows: int = 100,
                                           date_format: str = '%Y-%m-%d', granularity="D"):
    def calculate_date(end_date, start_date):
        if granularity == 'D':
            return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        if granularity == "H":
            return start_date + datetime.timedelta(
                hours=random.randint(0, (end_date - start_date).total_seconds() / 3600))

    # Convert string dates to datetime objects
    start_date = datetime.datetime.strptime(start_date, date_format)
    end_date = datetime.datetime.strptime(end_date, date_format)

    # Generate a list of random dates between the start and end date
    date_list = [calculate_date(end_date, start_date) for _ in range(num_rows)]

    # Create an initial DataFrame with one column of index values
    df = spark.range(num_rows).toDF("id")

    # Add random columns f1 to fN
    for i in range(1, num_columns + 1):
        df = df.withColumn(f"f{i}", f.rand())

    # Create a DataFrame for the date list
    date_df = spark.createDataFrame([(i, date) for i, date in enumerate(date_list)], ["id", "date"])

    # Join the original DataFrame with the date DataFrame on the id
    df = df.join(date_df, on="id").drop("id")

    # Add y column with random 0 or 1
    df = df.withColumn("y", (f.rand() * 2).cast(IntegerType()))

    # Drop the id column if you don't need it
    df = df.drop("id")

    return df


def generate_days_between(start_year, start_month, end_year, end_month):
    """
        Generate a list of dates between the start and end months of the given years.

        Args:
            start_year (int): The starting year.
            start_month (int): The starting month.
            end_year (int): The ending year.
            end_month (int): The ending month.

        Returns:
            list: A list of datetime objects for each day between the start and end dates.
        """
    # Create a datetime object for the starting date (first day of the starting month)
    start_date = datetime.datetime(start_year, start_month, 1)

    # Create a datetime object for the ending date (last day of the ending month)
    # We use the next month and subtract 1 day to get the last day of the ending month
    if end_month == 12:
        end_date = datetime.datetime(end_year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        end_date = datetime.datetime(end_year, end_month + 1, 1) - datetime.timedelta(days=1)

    # List to store all the dates
    all_days = []

    # Use a loop to go from start_date to end_date, adding one day at a time
    current_date = start_date
    while current_date <= end_date:
        all_days.append(current_date)
        current_date += datetime.timedelta(days=1)

    return all_days


def distribute_rows_across_days(total_rows, days_arr, min_rows_per_day, max_rows_per_day, partition_num,
                                add_data_to_fill_range):
    """
        Distribute rows across days while adhering to constraints and partitions.

        Args:
            total_rows (int): Total number of rows to distribute.
            days_arr (list): List of days to distribute rows across.
            min_rows_per_day (int): Minimum number of rows per day.
            max_rows_per_day (int): Maximum number of rows per day.
            partition_num (int): Number of partitions to create.
            add_data_to_fill_range (bool): Whether to add rows to meet the minimum row requirement.

        Returns:
            tuple: A dictionary of partition row distributions, total partitions, and added data count.
        """

    # Distribute rows evenly across the available days while adhering to min and max row constraints
    partition_row_distribution = {}
    remaining_rows = total_rows
    remaining_days = len(days_arr)
    data_added = 0
    # Calculate partitions per date
    if partition_num > remaining_days:
        partition_per_date = partition_num // remaining_days
    else:
        partition_per_date = remaining_days
    partition_index = 0

    row_created = 0
    # Distribute rows for each day
    for day in days_arr:
        rows_for_day = random.randint(min_rows_per_day, max_rows_per_day)
        rows_for_day = min(rows_for_day, remaining_rows)
        # adding min value
        if add_data_to_fill_range and 0 < rows_for_day < min_rows_per_day:
            data_added = data_added + min_rows_per_day - rows_for_day
            print(f"adding data remaining data {rows_for_day} setting data to min ")
            rows_for_day = min_rows_per_day
            remaining_rows = min_rows_per_day
        # Handle edge cases with no remaining rows
        if add_data_to_fill_range and remaining_rows == 0 and remaining_days > 0:
            print(f"adding data remaining days are {remaining_days} ")
            rows_for_day = min_rows_per_day
            data_added += min_rows_per_day
            remaining_rows = min_rows_per_day * remaining_days

        # Assign rows to partitions
        partition_index = partition_day_rows(day, partition_index, partition_per_date,
                                             partition_row_distribution, rows_for_day)
        remaining_rows -= rows_for_day
        row_created += rows_for_day
        remaining_days -= 1
    distributing_arr_size = len(partition_row_distribution)
    # Distribute any leftover rows evenly across partitions
    if remaining_rows > 0:
        print(f"there is left over rows {remaining_rows} distributing across partitions")
        remaining_rows_per_day = remaining_rows // distributing_arr_size
        for key, value in partition_row_distribution.items():
            if key == distributing_arr_size - 1:
                remaining_rows_per_day += remaining_rows % distributing_arr_size
            value[1] = value[1] + remaining_rows_per_day
            partition_row_distribution[key] = value
            row_created += remaining_rows_per_day

    print(f"Row Created {row_created}")

    return partition_row_distribution, distributing_arr_size, data_added


def partition_day_rows(day, partition_index, partition_per_date, partition_row_distribution, rows_for_day):
    """
        Assign rows for a given day across partitions.

        Args:
            day (datetime): The current day.
            partition_index (int): The starting partition index.
            partition_per_date (int): Number of partitions per date.
            partition_row_distribution (dict): Dictionary to store partition data.
            rows_for_day (int): Number of rows for the current day.

        Returns:
            int: Updated partition index.
        """
    partition_row = rows_for_day // partition_per_date
    for i in range(partition_per_date):
        if i == partition_per_date - 1:
            partition_row += rows_for_day % partition_per_date
        partition_row_distribution[partition_index] = [day, partition_row]
        partition_index += 1
    return partition_index


def create_large_simple_date_data(spark, total_rows, column_numbers, target_column_name, target_column_number,
                                  date_column_number=None, date_column_name="date", starting_month=0,
                                  starting_year=0, ending_month=0, max_rows_per_day=0, min_rows_per_day=0,
                                  add_data_to_fill_range=True):
    """
        Generate a large dataset with random numeric values, target labels, and date-based distribution.

        Args:
            spark (SparkSession): Spark session.
            total_rows (int): Total number of rows to generate.
            column_numbers (int): Number of columns in the dataset.
            target_column_name (str): Name of the target column.
            target_column_number (int): Index of the target column.
            date_column_number (int, optional): Index of the date column. Defaults to None.
            date_column_name (str, optional): Name of the date column. Defaults to "date".
            starting_month (int): Starting month for data generation.
            starting_year (int): Starting year for data generation.
            ending_month (int): Ending month for data generation.
            max_rows_per_day (int): Maximum rows per day.
            min_rows_per_day (int): Minimum rows per day.
            add_data_to_fill_range (bool): Whether to add rows to meet minimum constraints. Defaults to True.

        Returns:
            tuple: A PySpark DataFrame and a string representing the output path value.
        """

    num_partitions = int(spark.conf.get('spark.sql.shuffle.partitions'))
    print(f"values getting {total_rows} max rows {max_rows_per_day} min rows {min_rows_per_day} ")
    days_arr = generate_days_between(start_year=starting_year, start_month=starting_month, end_year=starting_year,
                                     end_month=ending_month)

    partition_row_distribution, calc_partition, row_added = distribute_rows_across_days(total_rows=total_rows,
                                                                                        days_arr=days_arr,
                                                                                        max_rows_per_day=max_rows_per_day,
                                                                                        min_rows_per_day=min_rows_per_day,
                                                                                        partition_num=num_partitions,
                                                                                        add_data_to_fill_range=add_data_to_fill_range)

    print(f"The calc partition {calc_partition}")
    print(f"row added {row_added}")
    print(f"day array size {len(days_arr)}")

    rdd = spark.sparkContext.parallelize(range(calc_partition), calc_partition)
    path_value = "nd"

    if date_column_number is not None:
        currentYear = datetime.datetime.now().year if starting_year == 0 else starting_year

        path_value = f"d_{currentYear}_{starting_month}_{ending_month}"

    def create_partition_data(partition_id):

        random.seed(partition_id)  # Ensure reproducibility across executors
        row_date = partition_row_distribution[partition_id]

        for _ in range(row_date[1]):
            value_list = []
            for i in range(column_numbers):
                if date_column_number is not None and i == date_column_number:
                    dt = row_date[0]
                    value_list.append(dt)
                elif i == target_column_number:
                    value_list.append(random.choices([0, 1], [0.99, 0.01])[0])
                else:
                    value_list.append(random.uniform(-1, 1))
            yield value_list

    # Generate data
    rdd = rdd.flatMap(create_partition_data)

    # Create column names
    column_names = [f"f{i}" for i in range(column_numbers)]
    if target_column_name:
        column_names[target_column_number] = target_column_name
    if date_column_number is not None:
        column_names[date_column_number] = date_column_name

    # Create DataFrame
    df = spark.createDataFrame(rdd, column_names)
    print(f"repartition data frame")
    df = df.repartition(num_partitions)

    return df, path_value


def create_large_simple_data_rdd(spark, base_number, column_numbers, target_column_name, target_column_number,
                                 power_number=2, date_column_number=None, date_column_name="date", starting_month=0,
                                 starting_year=0, ending_month=0):
    rdd = spark.sparkContext.parallelize([list(range(0, column_numbers))])
    path_value = "nd"
    if date_column_number is not None:
        currentMonth = datetime.datetime.now().month
        if starting_month > 0:
            currentMonth = starting_month
        currentYear = datetime.datetime.now().year
        if starting_year > 0:
            currentYear = starting_year
        range_month = monthrange(currentYear, currentMonth)[1]
        path_value = f"d_{currentYear}_{starting_month}_{ending_month}"

    def create_data(column_list):
        if starting_month > 0 and ending_month > 0:
            m_range = range_month
            month = currentMonth
        # print(f"this is the column list value  {column_list}")
        for c in range(0, base_number):
            value_list = []

            for i in range(0, len(column_list)):
                if date_column_number is not None and i == date_column_number:

                    if starting_month > 0 and ending_month > 0:
                        month = random.randint(starting_month, ending_month)
                        m_range = monthrange(currentYear, month)[1]
                    day = random.randint(1, m_range)
                    dt = datetime.datetime(currentYear, month, day)
                    value_list.insert(i, dt)
                    # print(f"this is the date value{i}  {value_list}")
                elif i == target_column_number:
                    value_list.insert(i, random.choices([0, 1], [0.99, 0.01])[0
                    ])
                else:
                    value_list.insert(i, random.uniform(-1, 1))
            yield value_list

    f = lambda column_list: create_data(column_list)

    # Increase the size of this loop to create more data.
    # The number of rows will be n ^ 2
    for _ in range(0, power_number):
        rdd = rdd.flatMap(f)
        rdd = rdd.repartition(int(spark.conf.get('spark.sql.shuffle.partitions')))
    # print(f"Lines created: {rdd.count()}")
    print(f"Lines created: {base_number ** power_number}")

    # write result to parquet file
    column_names = [f"f{i}" for i in range(0, column_numbers)]
    if target_column_name:
        column_names[target_column_number] = target_column_name
    if date_column_number:
        column_names[date_column_number] = date_column_name
    df = spark.createDataFrame(rdd, column_names)
    print(f"repartition data frame ")
    df = df.repartition(int(spark.conf.get('spark.sql.shuffle.partitions')))
    return df, path_value


def get_random_percent_indexes(array, n):
    # Calculate the number of indexes to return (30% of the length of the array)
    num_indexes_to_return = int(len(array) * n)
    # Shuffle the indexes of the array
    shuffled_indexes = list(range(len(array)))
    random.shuffle(shuffled_indexes)
    # Return the first 30% of shuffled indexes
    return shuffled_indexes[:num_indexes_to_return], [0.5] * num_indexes_to_return


# Function to get fully qualified name of a class
def get_fully_qualified_name(cls):
    return f"{cls.__module__}.{cls.__name__}"


# Function to get class object from fully qualified name
def get_class_from_fully_qualified_name(name):
    parts = name.split('.')
    module_name = '.'.join(parts[:-1])
    class_name = parts[-1]
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls
