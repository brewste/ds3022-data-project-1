import duckdb
import logging

#make new logger for this file
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clean.log'
)
logger = logging.getLogger(__name__)

#---STEP 1: Remove duplicates---
def remove_duplicates(con, table_name):
    # Count duplicate groups before cleaning
    before_duplicates = con.execute(f"""
        SELECT COUNT(*)
        FROM (
            SELECT *
            FROM {table_name}
            GROUP BY ALL
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]

    # Remove duplicates
    con.execute(f"""
        CREATE TABLE {table_name}_clean AS
        SELECT DISTINCT * FROM {table_name};
        DROP TABLE {table_name};
        ALTER TABLE {table_name}_clean RENAME TO {table_name};  
    """)
    logger.info(f"Removed duplicates from {table_name} table")

    # Verification query: count duplicate groups after cleaning
    after_duplicates = con.execute(f"""
        SELECT COUNT(*)
        FROM (
            SELECT *
            FROM {table_name}
            GROUP BY ALL
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]

    print(f"{table_name} duplicate groups: {before_duplicates} before, {after_duplicates} after")
    logger.info(f"{table_name} duplicate groups: {before_duplicates} before, {after_duplicates} after")



# STEP 2: Remove trips with zero passengers
def remove_zero_passenger_trips(con, table_name):
    # Count trips with zero passengers before cleaning
    before_zero_passengers = con.execute(f"""
        SELECT COUNT(*) 
        FROM {table_name} 
        WHERE passenger_count = 0
    """).fetchone()[0]

    # Remove trips with zero passengers
    con.execute(f"""
        DELETE FROM {table_name} 
        WHERE passenger_count = 0
    """)
    logger.info(f"Removed trips with zero passengers from {table_name} table")

    # Verification query: count trips with zero passengers after cleaning
    after_zero_passengers = con.execute(f"""
        SELECT COUNT(*) 
        FROM {table_name} 
        WHERE passenger_count = 0
    """).fetchone()[0]

    print(f"{table_name} trips with zero passengers: {before_zero_passengers} before, {after_zero_passengers} after")
    logger.info(f"{table_name} trips with zero passengers: {before_zero_passengers} before, {after_zero_passengers} after")



def clean_data():
    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance") 

        
        # ----- STEP 1: Remove duplicates -----
        
        remove_duplicates(con, "yellow_trips")
        remove_duplicates(con, "green_trips")

        # ----- STEP 2: Remove trips with zero passengers -----
        remove_zero_passenger_trips(con, "yellow_trips")
        remove_zero_passenger_trips(con, "green_trips")
   
   
   
   
   
   
   
   
   
   
   
    except Exception as e:
       print(f"Error during data cleaning: {e}")
       logger.error(f"Error during data cleaning: {e}")


if __name__ == "__main__":
    clean_data()




#
# #Step 3: remove zero mile trips
# #similar code but only changing passenger count; canbasically copy and paste
#
# before_miles = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips
#     WHERE trip_distance = 0
# """).fetchone()[0]
#
# con.execute("""DELETE FROM yellow_trips WHERE trip_distance = 0""")
#
# after_miles = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips
#     WHERE trip_distance = 0
# """).fetchone()[0]
#
# print(f'Before delete: {before_miles} After delete (verify): {after_miles}')
#
#
#
#
# #Step 4: remove trips over 100 miles 
# before_miles = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips
#     WHERE trip_distance > 100
# """).fetchone()[0]
#
# con.execute("""DELETE FROM yellow_trips WHERE trip_distance > 100""")
#
# after_miles = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips
#     WHERE trip_distance > 100
# """).fetchone()[0]
#
# print(f'Before delete: {before_miles} After delete (verify): {after_miles}')
#
#
#
# # Step 5: remove trips over 1 day
# before_duration = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips
#     WHERE date_diff('second', 'pickup_time', 'dropoff_time') > 86400
# """).fetchone()[0]
# print(f'Before delete: {before_duration}')
#
# con.execute("""DELETE FROM yellow_trips WHERE date_diff('second', 'pickup_time', 'dropoff_time') > 86400""")
#
# after_duration = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips
#     WHERE date_diff('second', 'pickup_time', 'dropoff_time') > 86400
# """).fetchone()[0]
#
# print(f'Before delete: {before_duration} After delete (verify): {after_duration}')
#
#
#
#
# # YOU HAVE TO DO ALL OF THIS FOR GREEN AS WELL!!