from pyspark.sql import SparkSession
import os
import delta

raw_data_path = os.environ.get("raw_data_path")
target_path = os.environ.get("target_path")

# Environment settings
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

def create_spark_session():
    """Initialize the Spark session with Delta Lake support"""
    builder = SparkSession.builder.appName("Crime Data Pipeline") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.sql.debug.maxToStringFields", "100") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.default.parallelism", "4")

    spark = delta.configure_spark_with_delta_pip(builder).getOrCreate()
    return spark
