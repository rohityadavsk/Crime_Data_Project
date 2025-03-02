import logging
import traceback
from config import *
from utils import *

# Log File Path
LOG_FILE = "../logs/pipeline.log"

# Configure logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to file
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting Spark session...")
        spark = create_spark_session()

        logger.info(f"Reading data from: {raw_data_path}")
        df_raw = read_csv_data(spark, raw_data_path)

        logger.info("Standardizing column names...")
        df_standardized = standardize_column_names(df_raw)

        logger.info("Performing transformations...")
        df_transformed = perform_transformations(df_standardized)

        record_count = df_transformed.count()
        logger.info(f"Total number of records: {record_count}")

        if record_count > 0:
            logger.info("\nWriting data in delta format...")
            write_data_delta(df_transformed)
        else:
            logger.warning("No records found after transformations.")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        logger.error(traceback.format_exc())  # Capture full stack trace
