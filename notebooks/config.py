from pyspark.sql import SparkSession
import os

RAW_DATA_PATH = os.environ.get("RAW_DATA_PATH")

# Environment settings
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

def create_spark_session():
    """Initialise the spark session"""
    spark = SparkSession.builder \
        .appName("LocalPysparkPipeline") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.sql.debug.maxToStringFields", "100") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.default.parallelism", "4") \
        .getOrCreate()

    return spark