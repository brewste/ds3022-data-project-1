# Set up log file for the full pipeline!
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='main_pipeline.log'
)
logger = logging.getLogger(__name__)


#import all the functions from the other files
from load import load_parquet_files
from clean import clean_data
from transform import transform
from analysis import analysis




#----DEFINE FUNCTION: Run the complete pipeline!!---
def run_pipeline():

    con = None

    #log all steps of the pipeline
    try:
        logger.info("Starting pipeline")

        load_parquet_files()
        logger.info("Load completed")

        clean_data()
        logger.info("Clean completed")

        transform()
        logger.info("Transform completed")

        analysis()
        logger.info("Analysis completed")

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()