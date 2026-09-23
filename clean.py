import duckdb
import logging

#make new logger for this file
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clean.log'
)
logger = logging.getLogger(__name__)

def clean_data():
    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance") 

        
        # ----- STEP 1: Remove duplicates -----
        
        #1a. YELLOW 
        # Count duplicate groups before cleaning
        before_duplicates = con.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT *
                FROM yellow_trips
                GROUP BY ALL
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        # Remove duplicates
        con.execute("""
            CREATE TABLE yellow_trips_clean AS
            SELECT DISTINCT * FROM yellow_trips;
            DROP TABLE yellow_trips;
            ALTER TABLE yellow_trips_clean RENAME TO yellow_trips;  
        """)
        logger.info("Removed duplicates from yellow_trips table")
        
        # Verification query: count duplicate groups after cleaning
        after_duplicates = con.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT *
                FROM yellow_trips
                GROUP BY ALL
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        print(f"Yellow duplicate groups: {before_duplicates} before, {after_duplicates} after")
        logger.info(f"Yellow duplicate groups: {before_duplicates} before, {after_duplicates} after")


        #1b. GREEN 
        # Count duplicate groups before cleaning
        before_duplicates = con.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT *
                FROM green_trips
                GROUP BY ALL
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        # Remove duplicates
        con.execute("""
            CREATE TABLE green_trips_clean AS
            SELECT DISTINCT * FROM green_trips;
            DROP TABLE green_trips;
            ALTER TABLE green_trips_clean RENAME TO green_trips;  
        """)
        logger.info("Removed duplicates from green_trips table")
        
        # Verification query: count duplicate groups after cleaning
        after_duplicates = con.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT *
                FROM green_trips
                GROUP BY ALL
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        print(f"Green duplicate groups: {before_duplicates} before, {after_duplicates} after")
        logger.info(f"Green duplicate groups: {before_duplicates} before, {after_duplicates} after")


   
   
   
   
   
   
   
   
   
   
   
    except Exception as e:
       print(f"Error during data cleaning: {e}")
       logger.error(f"Error during data cleaning: {e}")


if __name__ == "__main__":
    clean_data()



# # -----Step 2: remove trips with zero passengers
# before = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips 
#     WHERE passenger_count = 0
# """).fetchone()[0]
#
# con.execute("""DELETE FROM yellow_trips WHERE passenger_count = 0""")
#
# after = con.execute("""
#     SELECT COUNT(*) FROM yellow_trips 
#     WHERE passenger_count = 0
# """).fetchone()[0]
#
# print(f'Before delete: {before} After delete (verify): {after}')
# # you need to count rows after deletion!! for credit
#
#
#
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