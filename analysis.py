import duckdb
import logging
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='analysis.log'
)
logger = logging.getLogger(__name__)



#---DEFINE CONSTANTS: DAY_NAMES, MONTH_NAMES-----
DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] #dow aligns with index 0

MONTH_NAMES = ["","January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"] #months does not align with index 0, leave blank at 0



#--DEFINE REPORT---Report function is used in this file because there is more to print and log
def report (message):
    print(message)  #screen
    logger.info(message) # log




#--DEFINE largest_trip: get largest trip by CO2 emissions----
def largest_trip(con, label, table):
    
    # Get the largest single trip by CO2 emissions 
    row = con.execute(f"""
        SELECT trip_co2_kgs, trip_distance, pickup_time
        FROM {table}
        ORDER BY trip_co2_kgs DESC LIMIT 1  
    """).fetchone()
    report(f"Largest single trip of CO2 of 2024: [{label}] "
           f"{row[0]:.2f} kg CO2, {row[1]:.2f} miles, pickup at {row[2]}")
    



#---DEFINE heaviest_lightest: Get the heaviest and lightest average CO2 emissions by a specified column
def heaviest_lightest(con, label, table, column, description, names=None):

    # Get average CO2 emissions by specified column, order by highest average first
    #This will cover columns = [hour of day, day of week, week of year, and month of year]
    rows = con.execute(f"""
        SELECT {column}, AVG(trip_co2_kgs) AS avg_co2
        FROM {table} 
        GROUP BY {column} 
        ORDER BY avg_co2 DESC
    """).fetchall()

    #Grab highest (first item) and lowest (last item) of CO2 emission values 
    highest = rows[0]
    lowest = rows[-1]

    #If names are provided (like day names or month names), use them to get name for the highest and lowest values. 
    if names:
        highest_name = names[int(highest[0])]
        lowest_name = names[int(lowest[0])]
    # Otherwise, just use the numeric value from the column (hours and weeks).
    else:
        highest_name = highest[0]
        lowest_name = lowest[0]

    # Report the findings
    report(
        f"[{label}] Most carbon-heavy {description}: "
        f"{highest_name} with {highest[1]:.2f} kg average CO2 per trip")
    report(
        f"[{label}] Most carbon-light {description}: "
        f"{lowest_name} with {lowest[1]:.2f} kg average CO2 per trip")




#---GRAPHING SECTION------

#----Helper function: Get monthly totals for plotting
def get_monthly_totals(con, table):

    # Get total CO2 emissions by month
    rows = con.execute(f"""
        SELECT month_of_year, SUM(trip_co2_kgs) AS total_co2
        FROM {table}
        GROUP BY month_of_year
        ORDER BY month_of_year
    """).fetchall()
    months = [row[0] for row in rows]
    totals = [row[1] / 1000 for row in rows] #convert kg to metric tons

    #send lists to be used for plotting 
    return months, totals



#----DEFINE monthly_plot: Main line plot of monthly CO2 emissions ----
def monthly_plot(con,filename="co2_by_month_2024.png"):

    #prepare data - grab those montly totals
    yellow_months, yellow_totals = get_monthly_totals(con, "yellow_trips")
    green_months, green_totals = get_monthly_totals(con, "green_trips")

    #Create axis for plotting
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx() #we need a second axis because very differnt scales for yellow and green
   
    #Plot - yellow taxi line on first axis, green taxi line on second axis
    sns.lineplot(x=yellow_months, y=yellow_totals, ax=ax1, color='gold', label='Yellow Taxi')
    sns.lineplot(x=green_months, y=green_totals, ax=ax2, color='green', label='Green Taxi')

    #Labels and titles
    ax1.set_title("Monthly CO2 Emissions by Taxi Type - 2024")
    ax1.set_xlabel('Month of Year')
    ax1.set_ylabel('Total Yellow Taxi CO2 Emissions (tons)')
    ax2.set_ylabel('Total Green Taxi CO2 Emissions (tons)')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    #Set tick marks
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(MONTH_NAMES[1:], rotation=45) #skip blank index 0 in month_names

    #Save plot as file
    fig.savefig(filename, dpi = 150, bbox_inches='tight')
    plt.close(fig) 

    report(f"Plot written to {filename}")

   





#----FINAL EXECUTION: Execute analysis functions for both tables-----
def analysis():
    
    con = None
    try: 
        #connect to local DuckDB instance
        con = duckdb.connect("emissions.duckdb", read_only=True)
        logger.info("Connected to DuckDB instance")

        #Answering questions 1 through 5 on rubric
        for label, table in [("YELLOW", "yellow_trips"), ("GREEN", "green_trips")]:
            largest_trip(con, label, table)
            heaviest_lightest(con, label, table, column = "hour_of_day", description = "Hour of day")
            heaviest_lightest(con, label, table, column = "day_of_week", description = "Day of week", names=DAY_NAMES) 
            heaviest_lightest(con, label, table, column = "week_of_year", description = "Week of year")
            heaviest_lightest(con, label, table, column = "month_of_year", description = "Month of year", names=MONTH_NAMES)

        #Create the monthly plot for both taxi types
        monthly_plot(con)
        
        con.close()
    
    except Exception as e:
        report(f"Error during analysis: {e}")
        raise

if __name__ == "__main__":
    analysis()


