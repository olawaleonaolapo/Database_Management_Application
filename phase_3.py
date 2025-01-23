# Author: <Olawale Francis Onaolapo>
# 

##############################################################################
# IMPORTED LIBRARIES - FOR API WEATHER DATA DOWNLOAD
##############################################################################
import os
import sqlite3
import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta


##############################################################################
# FUNCTION TO MAKE THE SCRIPT LOCATION AS THE CURRENT WORKING DIRECTORY
##############################################################################
def change_to_script_directory():
    """
    Changes the current working directory to the directory where the script is located.
    """
    path_to_this_file = os.path.dirname(__file__)
    os.chdir(path_to_this_file)
    print("CURRENT WORKING DIRECTORY:", os.getcwd())


##############################################
# FUNCTION FOR CONNECTING TO THE DATABASE
##############################################
def db_connection(connection):
    """
    Establishes and returns a connection to the SQLite database.

    Args:
        connection: SQLite database connection object.

    Returns:
        sqlite3.Connection: Active database connection with row factory set.

    Raises:
        sqlite3.OperationalError: If a connection error occurs.
    """
    try:
        with sqlite3.connect(connection) as connection:
            connection.row_factory = sqlite3.Row
            connection.commit()
            return connection
    except sqlite3.OperationalError as ex:
        print(ex)


##############################################
# FUNCTION TO INITIALIZE THE DATABASE
##############################################
def initialize_db(connection):
    """
    Initializes the database structure by creating necessary columns if required .
    """
    with connection:
        cursor = connection.cursor()

        # Check if the sw_radiation column exists. Add the sw_radiation column if it does not exist
        pragma_info = cursor.execute("PRAGMA table_info(daily_weather_entries);")

        column_names = []
        for info in pragma_info:

            column_name = info['name']
            column_names.append(column_name)
        if "sw_radiation" not in column_names:
            cursor.execute("""
            ALTER TABLE daily_weather_entries ADD COLUMN sw_radiation REAL DEFAULT 0 NOT NULL;
            """)

    print("Database initialized successfully!")


###################################################################
# FUNCTION TO GET THE CITY DETAILS FROM GEOPY AND TIMEZONE FINDER
###################################################################
def get_city_details(city_name):
    """
    Get the latitude, longitude, country name, and timezone of a city using geopy and timezonefinder.

    Args:
        city_name (str): Name of the city.

    Returns:
        dict: A dictionary containing latitude, longitude, country name, and timezone.
    """
    city_geolocator = Nominatim(user_agent="onaolapofo")
    city_location = city_geolocator.geocode(city_name)

    if not city_location:
        raise ValueError(f"City '{city_name}' not found.")

    city_latitude, city_longitude = city_location.latitude, city_location.longitude
    city_country = city_location.address.split(",")[-1].strip()
    city_timezone_finder = TimezoneFinder()
    city_timezone = city_timezone_finder.timezone_at(lat=city_latitude, lng=city_longitude)

    if not city_timezone:
        raise ValueError(f"Timezone not found for city '{city_name}'.")

    # Adjust country name and timezone based on what already exist in the database
    if city_country == "United Kingdom":
        city_country = "Great Britain"
    if city_timezone == "Europe/Paris":
        city_timezone = "Europe/Berlin"

    return {"latitude": city_latitude, "longitude": city_longitude, "country": city_country, "timezone": city_timezone}


#################################################################
# FUNCTION TO VALIDATE DATES
#################################################################
def validate_dates(start_date, end_date):
    """
    Validates the start and end dates.

    Args:
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.

    Raises:
        ValueError: If the start date or end date is invalid based on the constraints.
    """
    current_date = datetime.now().date()
    two_days_before_today = current_date - timedelta(days=2)

    formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    if formatted_start_date > two_days_before_today:
        raise ValueError(f"The start date cannot be after two days before today's date: {two_days_before_today}.")
    if formatted_end_date > two_days_before_today:
        raise ValueError(f"The end date cannot be after two days before today's date: {two_days_before_today}.")
    if formatted_end_date <= formatted_start_date:
        raise ValueError("The end date must be after the start date.")

    print("Dates are valid!")


#####################################################################
# FUNCTION FOR RETRIEVING AND SAVING THE DATA INTO THE DATABASE
#####################################################################
def retrieve_and_store_weather_data(city_name, city_details, db_directory_n_name, start_date, end_date):
    """
    Retrieves weather data for a given city from the Open-Meteo API and stores it in the SQLite database.

    Args:
        city_name (str): Name of the city for which weather data is to be retrieved.
        city_details (dict): Dictionary containing the city's details, including:
            - latitude (float): Latitude of the city.
            - longitude (float): Longitude of the city.
            - country (str): Country where the city is located.
            - timezone (str): Timezone of the city.
        db_directory_n_name (str): Connection to the SQLite database file.
        start_date (str): Start date for the weather data to be retrieved (YYYY-MM-DD format).
        end_date (str): End date for the weather data to be retrieved (YYYY-MM-DD format).

    Process:
        1. Connects to the SQLite database and ensures the country and city exist in the respective tables.
        2. Updates city details (longitude, latitude, country_id) if discrepancies are found.
        3. Get weather data from the Open-Meteo API for the specified date range.
        4. Inserts or updates daily weather entries in the `daily_weather_entries` table, ensuring no duplicate entries.

    Raises:
        sqlite3.Error: If any database operation fails.
        Exception: For any unexpected errors during the API request or data processing.

    Prints:
        - Success messages for saving weather data.
        - Error messages if weather data retrieval fails or a database error occurs.
    """
    citi_latitude, citi_longitude = city_details["latitude"], city_details["longitude"]
    citi_country, citi_timezone = city_details["country"], city_details["timezone"]

    try:
        with sqlite3.connect(db_directory_n_name) as connection:
            cursor = connection.cursor()

            # Check if the country exists, reuse it if found
            country_id_column = cursor.execute("SELECT id FROM countries WHERE name = ?", (citi_country,))
            country_id = None
            for row in country_id_column:
                country_id = row[0]
                break
            if not country_id:
                cursor.execute("INSERT INTO countries (name, timezone) VALUES (?, ?)", (citi_country, citi_timezone))
                country_id = cursor.lastrowid

            # Check if the city exists, reuse it if found
            city_data = cursor.execute("SELECT id, longitude, latitude, country_id FROM cities WHERE name = ?", (city_name,))
            city_id = None
            for row in city_data:
                city_id, existing_longitude, existing_latitude, existing_country_id = row
                
                # Update the city's longitude and latitude if they differ
                if existing_longitude != citi_longitude or existing_latitude != citi_latitude:
                    cursor.execute("""
                    UPDATE cities SET longitude = ?, latitude = ? WHERE id = ?;
                    """, (citi_longitude, citi_latitude, city_id))

            # Check if the country ID is different and update if necessary
                if existing_country_id != country_id:
                    cursor.execute("""
                    UPDATE cities SET country_id = ? WHERE id = ?;
                    """, (country_id, city_id))
                break
            else:
                cursor.execute("""
                INSERT INTO cities (name, longitude, latitude, country_id)
                VALUES (?, ?, ?, ?);
                """, (city_name, citi_longitude, citi_latitude, country_id))
                city_id = cursor.lastrowid

            # OPEN METEO API URL
            url = (
                f"https://archive-api.open-meteo.com/v1/archive?"
                f"latitude={citi_latitude}&longitude={citi_longitude}&start_date={start_date}&end_date={end_date}"
                f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,shortwave_radiation_sum"
                f"&timezone={citi_timezone}"
            )

            response = requests.get(url)
            if response.status_code == 200:
                open_meteo_historical_weather_data = response.json()

                # Process and store weather data
                for retrieved_data, date in enumerate(open_meteo_historical_weather_data["daily"]["time"]):
                    min_temp = open_meteo_historical_weather_data["daily"]["temperature_2m_min"][retrieved_data]
                    max_temp = open_meteo_historical_weather_data["daily"]["temperature_2m_max"][retrieved_data]
                    mean_temp = open_meteo_historical_weather_data["daily"]["temperature_2m_mean"][retrieved_data]
                    precipitation = open_meteo_historical_weather_data["daily"]["precipitation_sum"][retrieved_data]
                    radiation = open_meteo_historical_weather_data["daily"]["shortwave_radiation_sum"][retrieved_data]

                    # Check if row already exists with valid date and city_id
                    cursor.execute("""
                    SELECT id, date, city_id FROM daily_weather_entries WHERE date = ? AND city_id = ?;
                    """, (date, city_id))
                    existing_rows = cursor.execute("""
                    SELECT id, date, city_id FROM daily_weather_entries WHERE date = ? AND city_id = ?;
                    """, (date, city_id))
                    row_exists = False
                    for _ in existing_rows:
                        row_exists = True
                        break

                    if row_exists:
                        # Update row only if it has null or zero values in any of the columns
                        cursor.execute("""
                        UPDATE daily_weather_entries
                        SET
                            min_temp = CASE WHEN min_temp = 0 OR min_temp IS NULL THEN ? ELSE min_temp END,
                            max_temp = CASE WHEN max_temp = 0 OR max_temp IS NULL THEN ? ELSE max_temp END,
                            mean_temp = CASE WHEN mean_temp = 0 OR mean_temp IS NULL THEN ? ELSE mean_temp END,
                            precipitation = CASE WHEN precipitation = 0 OR precipitation IS NULL THEN ? ELSE precipitation END,
                            sw_radiation = CASE WHEN sw_radiation = 0 OR sw_radiation IS NULL THEN ? ELSE sw_radiation END
                        WHERE date = ? AND city_id = ?;
                        """, (min_temp, max_temp, mean_temp, precipitation, radiation, date, city_id))
                    else:
                        cursor.execute("""
                        INSERT INTO daily_weather_entries (
                            date, min_temp, max_temp, mean_temp, precipitation, sw_radiation, city_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?);
                        """, (date, min_temp, max_temp, mean_temp, precipitation, radiation, city_id))

                print(f"Weather data for {city_name} saved successfully!")
            else:
                print(f"Failed to get weather data for {city_name}. HTTP Status Code: {response.status_code}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")


############################################################
# FUNCTION TO SWAP THE COLUMN NAMES - NOT USED
############################################################
def swap_longitude_latitude_columns(connection):
    """
    Swaps the longitude and latitude columns in the `cities` table of the database.

    Args:
        connection: A SQLite database connection object.

    Process:
        1. Temporarily disables foreign key constraints.
        2. Creates a new table `cities_new` with the swapped column structure.
        3. Copies data from the old `cities` table to the new one with longitude 
           and latitude swapped.
        4. Drops the old `cities` table.
        5. Renames `cities_new` to `cities`.
        6. Re-enables foreign key constraints.

    Returns:
        None

    Raises:
        sqlite3.OperationalError: If an error occurs during database operations.

    Prints:
        A success message indicating that the swap operation was completed.
    """
    with connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=off;")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            longitude TEXT NOT NULL,
            latitude TEXT NOT NULL,
            country_id INTEGER NOT NULL,
            FOREIGN KEY (country_id) REFERENCES countries (id) ON DELETE SET NULL
        );
        """)
        cursor.execute("""
        INSERT INTO cities_new (id, name, latitude, longitude, country_id)
        SELECT id, name, longitude, latitude, country_id FROM cities;
        """)
        cursor.execute("DROP TABLE cities;")
        cursor.execute("ALTER TABLE cities_new RENAME TO cities;")
        cursor.execute("PRAGMA foreign_keys=on;")
    print("The Longitude and the latitude columns in the daily_weather_entries table swapped successfully!")


#################################################################
# DATA REQUEST EXECUTION SECTION - REFERENCED AS MAIN
#################################################################
def main():
    """
    Main function that drives the weather data retrieval and database update process.

    The function performs the following tasks:
    1. Changes the working directory to the location of the script.
    2. Establishes a connection to the SQLite database.
    3. Initializes the database / ensures necessary tables are set up.
    4. Optionally swaps longitude and latitude columns if needed.
    5. Prompts the user to input a date range (start date and end date) for the weather data.
    6. Validates the entered dates to ensure they are within the available range.
    7. Retrieves weather data for the predefined list of cities.
    8. For each city, get city details, retrieves weather data from the Open-Meteo API, and stores it in the database.
    9. Catches and prints any errors encountered during the process.

    Raises:
        ValueError: If the user enters invalid date input.
        Exception: If an unexpected error occurs during data retrieval or database operations.

    Prints:
        - Success messages when weather data is saved successfully.
        - Error messages if issues occur.
    """

    change_to_script_directory()
    db_directory_n_name = "db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
    connection = db_connection(db_directory_n_name)

    if not connection:
        print("Failed to connect to the database.")
        return

###########################################################################
    # SWAPPING THE LONGITUDE AND LATITUDE COLUMNS NAMES
    # ONLY UNCOMMENT SWAP_LONGITUDE_LATITUDE COLUMNS FUNCTION IF NEEDED
###########################################################################
#    swap_longitude_latitude_columns(connection)

    cities = ["Lagos", "Middlesbrough", "London", "Leeds", "Paris", "Toulouse"]

    try:
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

        validate_dates(start_date, end_date)

        initialize_db(connection)

        for city_name in cities:
            try:
                city_details = get_city_details(city_name)
                retrieve_and_store_weather_data(city_name, city_details, db_directory_n_name, start_date, end_date)
            except ValueError as e:
                print(e)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
