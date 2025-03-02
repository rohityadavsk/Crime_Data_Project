from pyspark.sql import SparkSession
import os

raw_data_path = os.environ.get("raw_data_path")
target_path = os.environ.get("target_path")

# Environment settings
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

def create_spark_session():
    """Initialise the spark session"""
    spark = SparkSession.builder \
        .appName("Crime Data Pipeline") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:3.0.0") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.sql.debug.maxToStringFields", "100") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.default.parallelism", "4") \
        .getOrCreate()

    return spark