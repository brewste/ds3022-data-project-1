import duckdb
import os
import logging

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load.log'
)
logger = logging.getLogger(__name__)

def load_parquet_files():

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance")

        # Make yellow taxi table


        # Make green taxi table

        #make vehicle emissions table
        con.execute("""
           DROP TABLE IF EXISTS vehicle_emissions;
            CREATE TABLE vehicle_emissions AS
            SELECT * FROM read_csv_auto(
            'data/vehicle_emissions.csv'
            );
        """)

        n = con.execute(
            "SELECT COUNT(*) FROM vehicle_emissions"
            ).fetchone()[0]

        logger.info(f"vehicle_emissions: {n} rows loaded")



        #Count total rows?


    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    load_parquet_files()