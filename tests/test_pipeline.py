import pytest
from notebooks.utils import *

# Create a Spark session for testing
@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .appName("TestPysparkPipeline") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.sql.debug.maxToStringFields", "100") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "2g") \
        .config("spark.default.parallelism", "4") \
        .getOrCreate()
    yield spark
    spark.stop()

# Test the standardization of column names
def test_standardize_column_names(spark):
    data = [("John Doe", 28), ("Jane Smith", 34)]
    columns = ["Full Name", "Age"]
    df = spark.createDataFrame(data, columns)

    standardized_df = standardize_column_names(df)

    # Check if column names were standardized
    assert "full_name" in standardized_df.columns
    assert "age" in standardized_df.columns

# Test if CSV file reading works
def test_read_csv_data(spark):
    df = read_csva_data(spark, raw_data_path)

    # Check if DataFrame is not empty
    assert df.count() > 0




