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
        


        # VEHICLE EMISSIONS TABLE
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
        print(f"vehicle_emissions: {n} rows loaded")


        

        # YELLOW TAXI TABLE

        # Create yellow taxi table
        con.execute("""
            DROP TABLE IF EXISTS yellow_trips;
            
            CREATE TABLE yellow_trips (
                    VendorID INTEGER,
                    pickup_time TIMESTAMP,
                    dropoff_time TIMESTAMP,
                    passenger_count INTEGER,
                    trip_distance FLOAT
            );
        """)
        logger.info("Created yellow_trips table")
       
        # Load all 12 months of 2024 yellow taxi data using for loop
        for month in range(1, 13):
            url = (
                f"https://d37ci6vzurychx.cloudfront.net/trip-data/"
                f"yellow_tripdata_2024-{month:02d}.parquet"
            )

            con.execute(f"""
                INSERT INTO yellow_trips
                SELECT 
                    VendorID,
                    tpep_pickup_datetime AS pickup_time,
                    tpep_dropoff_datetime AS dropoff_time,
                    passenger_count,
                    trip_distance
                FROM read_parquet('{url}');
            """)
            logger.info(f"Loaded yellow taxi data for month {month:02d}")
        

        #Get raw count of rows in yellow_trips table
        n = con.execute(
            "SELECT COUNT(*) FROM yellow_trips"
            ).fetchone()[0]
        logger.info(f"yellow_trips: {n} rows loaded")
        print(f"yellow_trips: {n} rows loaded")

    


    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    load_parquet_files()