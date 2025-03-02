import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pyspark.sql.functions import *
from config import *
from functools import wraps
import time

def time_it(func):
    """
    Decorator to measure the execution time of a function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f'{func.__name__} function took {duration:.2f} seconds')
        return result
    return wrapper


def standardize_column_names(df: DataFrame) -> DataFrame:
    """
    Standardize column names by converting them to lowercase and replacing spaces with underscores
    Args:
        df (DataFrame): Dataframe to standardize
    Returns:
        DataFrame: Dataframe with standardized column names
    """
    rename_exprs = {col: col.strip().lower().replace(' ', '_') for col in df.columns}
    return df.select([col(old).alias(new) for old, new in rename_exprs.items()])

@time_it
def read_csv_data(spark, path: str):
    """Read csv data into a spark dataframe"""
    try:
        return spark.read.format('csv') \
            .options(header='true',
                     inferSchema='true') \
            .load(path)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        raise

@time_it
def perform_transformations(df: DataFrame):
    """Perform transformations"""
    df_final = df \
        .withColumn('date_rptd', to_date(to_timestamp(col('date_rptd'), 'MM/dd/yyyy hh:mm:ss a'))) \
        .withColumn('date_occ', to_date(to_timestamp(col('date_occ'), 'MM/dd/yyyy hh:mm:ss a'))) \
        .withColumn('time_occ', date_format(expr("make_timestamp(1970, 1, 1, int(time_occ/100), time_occ%100, 0)"), 'h:mm a')) \
        .filter(col("vict_age").cast("int").isNotNull())
    return df_final


@time_it
def write_data_delta(df: DataFrame, path: str):
    """Write transformed data in delta format"""
    df.write.format('delta').mode('overwrite').save(path)
    print('Successfully wrote to delta format')