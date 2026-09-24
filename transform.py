import duckdb
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("transform.log"), logging.StreamHandler()])

logger = logging.getLogger(__name__)



#---STEP 1: Add new columns to the table for calculated values---
def add_columns (con, table):
    
    #We need to calculate/extract these six values, so we will add them as new columns to the table!
    columns = [
        "trip_co2_kgs DOUBLE",
        "avg_mph DOUBLE",
        "hour_of_day INTEGER",
        "day_of_week INTEGER",
        "week_of_year INTEGER",
        "month_of_year INTEGER"
    ]

    #Add all six new columns if they don't already exist.
    for column in columns:
        con.execute(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column};")
    logger.info(f"{table}: {columns} exists in the table.")




#---STEP 2: Transform the data to calculate the new values---
def transform_data(con, table, label):

    #Calculate trip_co2_kgs:
    con.execute(f"""
            UPDATE {table} SET trip_co2_kgs = (
                SELECT ({table}.trip_distance * ve.co2_grams_per_mile) / 1000
                FROM vehicle_emissions AS ve
                WHERE ve.vehicle_type = '{label}'
            );
            """)

    #Calculate avg_mph:
    con.execute(f"""
            UPDATE {table} SET avg_mph = trip_distance / 
            date_diff('second', pickup_time, dropoff_time) * 3600
        WHERE date_diff('second', pickup_time, dropoff_time) > 0;   --Avoid division by zero
    """)

    # Calculate hour_of_day:
    con.execute(f"UPDATE {table} SET hour_of_day = date_part('hour', pickup_time);")

    # Calculate day_of_week:
    con.execute(f"UPDATE {table} SET day_of_week = date_part('dow', pickup_time);")

    # Calculate week_of_year:
    con.execute(f"UPDATE {table} SET week_of_year = date_part('week', pickup_time);")

    # Calculate month_of_year:
    con.execute(f"UPDATE {table} SET month_of_year = date_part('month', pickup_time);")



#---FINAL STEP: Execute functions----
def transform():
    con = None
    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database="emissions.duckdb", read_only=False)
        logger.info("Connected to DuckDB instance") 

        # Execute transformations for each table (yellow or green table) 
        # and each label ("yellow_taxi" or "green_taxi" in vehicle emissions table) using functions above
        for label, table in [
            ("yellow_taxi", "yellow_trips"),
            ("green_taxi", "green_trips")
        ]:
            add_columns(con, table)
            transform_data(con, table, label)
            logger.info(f"{table}: transformations completed")


    except Exception as e:
        logger.error(f"Error during transformation: {e}")


if __name__ == "__main__":
    transform()