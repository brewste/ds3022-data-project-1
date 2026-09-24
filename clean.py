import duckdb
import logging

#make new logger for this file
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clean.log'
)
logger = logging.getLogger(__name__)



#----DEFINE FUNCTION: Remove duplicates-----
def remove_duplicates(con, table_name):
    
    # Count duplicate groups before cleaning
    before_duplicates = con.execute(f"""
        SELECT COUNT(*) FROM 
        (SELECT * FROM {table_name} GROUP BY ALL HAVING COUNT(*) > 1)
    """).fetchone()[0]

    #Execution: drop table if exists
    con.execute(f"DROP TABLE IF EXISTS {table_name}_clean;")

    #Execution: remove duplicates 
    con.execute(f"""
        CREATE TABLE {table_name}_clean AS
        SELECT DISTINCT * FROM {table_name};
        DROP TABLE {table_name};
        ALTER TABLE {table_name}_clean RENAME TO {table_name};  
    """)
    logger.info(f"Removed duplicates from {table_name} table")

    # Verification query- count after cleaning
    after_duplicates = con.execute(f"""
        SELECT COUNT(*) FROM (
            SELECT * FROM {table_name} GROUP BY ALL HAVING COUNT(*) > 1)
    """).fetchone()[0]
    print(f"{table_name} duplicate groups: {before_duplicates} before, {after_duplicates} after")
    logger.info(f"{table_name} duplicate groups: {before_duplicates} before, {after_duplicates} after")



# #----DEFINE FUNCTION: Remove trips with zero passengers-----
def remove_zero_passenger_trips(con, table_name):
    
    # Count before cleaning
    before_zero_passengers = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE passenger_count = 0
    """).fetchone()[0]

    # Execution: Remove trips with zero passengers
    con.execute(f"""
        DELETE FROM {table_name} 
        WHERE passenger_count = 0
    """)
    logger.info(f"Removed trips with zero passengers from {table_name} table")

    # Verification query- count after cleaning
    after_zero_passengers = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE passenger_count = 0
    """).fetchone()[0]
    print(f"{table_name} trips with zero passengers: {before_zero_passengers} before, {after_zero_passengers} after")
    logger.info(f"{table_name} trips with zero passengers: {before_zero_passengers} before, {after_zero_passengers} after")



#----DEFINE FUNCTION: Remove trips with zero miles-----
def remove_zero_mile_trips(con, table_name):
    
    # Count before cleaning
    before_zero_miles = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE trip_distance = 0
    """).fetchone()[0]

    # Execution: Remove trips with zero miles
    con.execute(f"""
        DELETE FROM {table_name} 
        WHERE trip_distance = 0
    """)
    logger.info(f"Removed trips with zero miles from {table_name} table")

    # Verification query- count after cleaning
    after_zero_miles = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE trip_distance = 0
    """).fetchone()[0]
    print(f"{table_name} trips with zero miles: {before_zero_miles} before, {after_zero_miles} after")
    logger.info(f"{table_name} trips with zero miles: {before_zero_miles} before, {after_zero_miles} after")



#---DEFINE FUNCTION: Remove trips with over 100 miles-----
def remove_over_100_mile_trips(con, table_name):
    
    # Count trips before cleaning
    before_over_100_miles = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE trip_distance > 100
    """).fetchone()[0]

    # Execution: Remove trips with over 100 miles
    con.execute(f"""
        DELETE FROM {table_name} 
        WHERE trip_distance > 100
    """)
    logger.info(f"Removed trips with over 100 miles from {table_name} table")

    # Verification query- count after cleaning
    after_over_100_miles = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE trip_distance > 100
    """).fetchone()[0]
    print(f"{table_name} trips with over 100 miles: {before_over_100_miles} before, {after_over_100_miles} after")
    logger.info(f"{table_name} trips with over 100 miles: {before_over_100_miles} before, {after_over_100_miles} after")



#----DEFINE FUNCTION: Remove trips over 1 day (86400 seconds)-----
def remove_trips_over_1_day(con, table_name):

    # Count trips before cleaning
    before_over_1_day = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE date_diff('second', pickup_time, dropoff_time) > 86400 
    """).fetchone()[0]

    # Execution: Remove trips over 1 day
    con.execute(f"""
        DELETE FROM {table_name} 
        WHERE date_diff('second', pickup_time, dropoff_time) > 86400
    """)
    logger.info(f"Removed trips over 1 day from {table_name} table")

    # Verification query- count after cleaning
    after_over_1_day = con.execute(f"""
        SELECT COUNT(*) FROM {table_name} 
        WHERE date_diff('second', pickup_time, dropoff_time) > 86400
    """).fetchone()[0]
    print(f"{table_name} trips over 1 day: {before_over_1_day} before, {after_over_1_day} after")
    logger.info(f"{table_name} trips over 1 day: {before_over_1_day} before, {after_over_1_day} after")




#---FINAL STEP: Execute functions for both tables-----
def clean_data():
    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance") 

        for table in ["yellow_trips", "green_trips"]:
        
        # ----- STEP 1: Remove duplicates -----
            remove_duplicates(con, table)
    
        # ----- STEP 2: Remove trips with zero passengers -----
            remove_zero_passenger_trips(con, table)
        
        #---- STEP 3: Remove trips with zero miles --
            remove_zero_mile_trips(con, table)

        #---- STEP 4: Remove trips with over 100 miles --- 
            remove_over_100_mile_trips(con, table)

        #---- STEP 5: Remove trips over 1 day (86400 seconds) ---
            remove_trips_over_1_day(con, table)


    except Exception as e:
       print(f"Error during data cleaning: {e}")
       logger.error(f"Error during data cleaning: {e}")
       raise


if __name__ == "__main__":
    clean_data()


