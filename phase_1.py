# Author: <Olawale Francis Onaolapo>
# 

##############################################################################
# IMPORTED LIBRARIES - FOR DATABASE QUERIES
##############################################################################
import os
import sqlite3


# Phase 1 - Starter
#
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory
'''


def select_all_countries(connection):
    # Queries the database and selects all the countries
    # stored in the countries table of the database.
    # The returned results are then printed to the
    # console.
    try:
        # Define the query
        query = "SELECT * FROM countries"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Return the data in the countries table
        return results

        # Iterate over the results and display the results.
        # for row in results:
        #     print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)


def select_all_cities(connection):
    """
    Retrieves all records from the 'cities' table in the database.

    Args:
        connection: A SQLite database connection object.

    Returns:
        sqlite3.Cursor: Cursor object containing the query results,
        which can be iterated to retrieve city details.

    Raises:
        sqlite3.OperationalError: If an error occurs during the query execution.
    """
    try:
        # Define the query
        query = "SELECT * FROM cities"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Return the records in the cities table
        return results

        # Iterate over the results and display the results.
        #  for row in results:
        #     print(f"City Id: {row['id']} -- City Name: {row['name']} -- City Longitude: {row['longitude']} -- "
        # f"City Latitude: {row['latitude']} -- Country ID: {row['country_id']}")

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Good
'''


def average_annual_temperature(connection, city_id, year):
    """
    Calculates the average annual temperature for a specific city and year.

    Args:
        connection: SQLite database connection object.
        city_id: ID of the city.
        year: Year to filter the data (YYYY).

    Returns:
        sqlite3.Cursor: Query results, iterable to retrieve city details and temperature.

    Raises:
        sqlite3.OperationalError: If a database query error occurs.
    """
    try:
        # Define the query
        query = """
            SELECT AVG(dw.mean_temp) AS annual_mean_temperature, dw.city_id AS city_id, strftime('%Y', dw.date) AS year, c.name AS city_name
            FROM [daily_weather_entries] AS dw
            JOIN cities AS c
            ON c.id == dw.city_id
            WHERE city_id == ?
            AND year like ?
        """

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query, (city_id, year))

        # Return the temperature and other records
        return results

        # Iterate over the results and display the results.
        # for row in results:
        #    print(f"City Id: {row['city_id']} -- City Name: {row['city_name']} -- Year: {row['year']} -- Annual Mean Temperature: {row['annual_mean_temperature']:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)


def average_seven_day_precipitation(connection, city_id, start_date):
    """
Calculates the average precipitation over seven days for a specific city, starting from a given date.

Args:
    connection: SQLite database connection object.
    city_id: ID of the city.
    start_date: Start date (YYYY-MM-DD) for the seven-day period.

Returns:
    sqlite3.Cursor: Query results, iterable to retrieve city details and precipitation data.

Raises:
    sqlite3.OperationalError: If a database query error occurs.
"""
    try:
        # Define the query
        query = """
            SELECT AVG(dw.precipitation) AS average_seven_day_precipitation, dw.city_id AS city_id, dw.date AS start_date, c.name AS city_name
            FROM [daily_weather_entries] AS dw
            JOIN cities AS c
            ON c.id == dw.city_id
            WHERE city_id == ?
            AND start_date >= ?
            AND start_date <= date(?, '+6 days')
            """

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query, (city_id, start_date, start_date))

        # return the city details and precipitation data
        return results

        # Iterate over the results and display the results.
        # for row in results:
        #    print(f"City Id: {row['city_id']} -- City Name: {row['city_name']} -- Seven Days Starting From: {row['start_date']} -- Average Seven Day Precipitation: {row['average_seven_day_precipitation']:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Very good
'''


def average_mean_temp_by_city(connection, date_from, date_to):
    """
    Calculates the average mean temperature for all cities within a specified date range.

    Args:
        connection: SQLite database connection object.
        date_from: Start date (YYYY-MM-DD) of the range.
        date_to: End date (YYYY-MM-DD) of the range.

    Returns:
        sqlite3.Cursor: Query results, iterable to retrieve city details and temperature data.

    Raises:
        sqlite3.OperationalError: If a database query error occurs.
    """
    try:
        # Define the query
        query = """
            SELECT AVG(dw.mean_temp) AS average_mean_temperature, dw.city_id AS city_id, dw.date AS date, c.name AS city_name
            FROM [daily_weather_entries] AS dw
            JOIN cities AS c
            ON c.id == dw.city_id
            WHERE dw.date >= ?
            AND dw.date <= ?
            Group by city_id
        """

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query, (date_from, date_to))

        # Return temperature and other information
        return results

        # Iterate over the results and display the results.
        # for row in results:
        #    print(f"City Id: {row['city_id']} -- City Name: {row['city_name']} -- Date From: {date_from} -- Date To: {date_to} -- Average Mean Temperature: {row['average_mean_temperature']:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)


def average_annual_precipitation_by_country(connection, year):
    """
    Calculates the average annual precipitation for each country for a specified year.

    Args:
        connection: SQLite database connection object.
        year: The year (YYYY) for which the average precipitation is calculated.

    Returns:
        sqlite3.Cursor: Query results, iterable to retrieve country details and precipitation data.

    Raises:
        sqlite3.OperationalError: If a database query error occurs.
    """
    try:
        # Define the query
        query = """
            SELECT AVG(dw.precipitation) AS average_annual_precipitation, strftime('%Y', dw.date) AS year, ct.id, ct.name
            FROM [daily_weather_entries] AS dw
            JOIN cities AS c
            ON c.id == dw.city_id
            JOIN countries AS ct
            ON ct.id == c.country_id
            WHERE strftime('%Y', dw.date) LIKE ? 
            GROUP BY ct.id
            """

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query, (year,))

        # Return the precipitation and other data
        return results

        # Iterate over the results and display the results.
        # for row in results:
        #    print(f"Country Id: {row['id']} -- Country Name: {row['name']} --Year: {row['year']}-- Average Annual Precipitation: {row['average_annual_precipitation']:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Excellent

You have gone beyond the basic requirements for this aspect.
'''


#########################################################################
# SUPPORTING FUNCTIONS USED IN PHASE 1 AND PHASE 2
#########################################################################
def get_date_input():
    """
    Prompts the user to enter a start and end date.
    Returns:
        tuple: (start_date, end_date)
    """
    date_from = input("Please, specify the start date in YYYY-MM-DD format: ")
    date_to = input("Please, specify the end date in YYYY-MM-DD format: ")
    return date_from, date_to


def extract_cities(connection):
    """Extract all city IDs and city names from the database."""
    all_cities = select_all_cities(connection)

    city_ids = []
    city_names = []
    for city in all_cities:
        city_ids.append(city['id'])
        city_names.append(city['name'])
    return city_ids, city_names


def display_available_cities(connection):
    """
    Displays the available cities in the database, ordered by ID, as a list.
    """
    print("\nAvailable Cities in the format: [City ID = City Name]")
    cities_table = select_all_cities(connection)

    city_list = []

    for row in cities_table:
        city_entry = f"{row['id']} = {row['name']}"
        city_list.append(city_entry)

    print(f"[{'; '.join(city_list)}]")


def validate_city_id(city_id, city_ids):
    """
    Validates a user-provided city ID against the list of valid city IDs.

    Args:
        city_id (int): The city ID provided by the user.
        city_ids (list): The list of valid city IDs.

    Returns:
        tuple:
            - bool: True if the city ID is valid, False otherwise.
            - str: An error message if the city ID is invalid; an empty string if valid.

    Validation Criteria:
        1. The city ID must exist in the provided `city_ids` list.
    """
    if city_id not in city_ids:
        return False, f"Invalid City ID. Please choose from the following IDs: {city_ids}."
    return True, ""


def db_distinct_years(connection):
    """
    Retrieves a list of distinct years from the 'daily_weather_entries' table.

    Args:
        connection: SQLite database connection object.

    Returns:
        list: A list of distinct years as strings.

    Raises:
        sqlite3.OperationalError: If a database query error occurs.
    """
    try:
        query = "SELECT DISTINCT(strftime('%Y', date)) AS distinct_year FROM [daily_weather_entries]"
        cursor = connection.cursor()
        results = cursor.execute(query)

        distinct_years = []
        for record in results:
            distinct_years.append(record['distinct_year'])

        return distinct_years
    except sqlite3.OperationalError as ex:
        print(ex)
        return []


def select_dates(connection):
    """
    Retrieves all available dates from the database, formatted correctly.
    """
    try:
        query = "SELECT DISTINCT strftime('%Y-%m-%d', date) AS db_date FROM [daily_weather_entries]"
        cursor = connection.cursor()
        results = cursor.execute(query)

        available_dates = []

        for row in results:
            db_date = row['db_date']
            available_dates.append(db_date)
        return available_dates
    except sqlite3.OperationalError as ex:
        print(ex)
        return []


def validate_db_dates(date_from, date_to, available_dates):
    """
    Validates the user-provided dates against the available dates.

    Args:
        date_from (str): Start date provided by the user.
        date_to (str): End date provided by the user.
        available_dates (list): List of valid dates from the database.

    Returns:
        bool: True if the dates are valid, False otherwise.
        str: Error message if dates are invalid.
    """
    if date_from not in available_dates or date_to not in available_dates:
        return False, f"Invalid dates. Please choose dates within the range: {min(available_dates)} - {max(available_dates)}."
    if date_from > date_to:
        return False, "Start date cannot be after the end date. Please re-enter the dates."
    return True, ""


def validate_year(year, distinct_years):
    """
    Validates a user-provided year against a list of distinct valid years.

    Args:
        year (str): The year input provided by the user, expected as a 4-digit string.
        distinct_years (list): A list of valid years available in the database or context.

    Returns:
        tuple:
            - bool: True if the year is valid, False otherwise.
            - str: An error message if the year is invalid; an empty string if valid.

    Validation Criteria:
        1. The year must be a 4-digit numeric string.
        2. The year must exist in the provided `distinct_years` list.
    """
    if len(year) != 4 or not year.isdigit():
        return False, "Invalid year format. Enter a 4-digit year."
    if year not in distinct_years:
        return False, f"Invalid year. Available years: {distinct_years}."
    return True, ""


def validate_user_inputs(connection, date_from, date_to, city_id):
    """
    Validates user-provided inputs for the date range and city ID.

    Args:
        connection: SQLite database connection object.
        date_from (str): Start date provided by the user.
        date_to (str): End date provided by the user.
        city_id (int): City ID provided by the user.

    Returns:
        bool: True if all inputs are valid, False otherwise.
        str: Error message if any input is invalid.
    """
    available_dates = select_dates(connection)
    city_ids, _ = extract_cities(connection)

    date_validation, date_error = validate_db_dates(date_from, date_to, available_dates)
    if not date_validation:
        return False, date_error

    city_validation, city_error = validate_city_id(city_id, city_ids)
    if not city_validation:
        return False, city_error

    return True, ""


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


##############################################################################
# FUNCTION FOR CONNECTING TO THE DATABASE - IN USE BY ALL THE OTHER FUNCTIONS
##############################################################################
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


#####################################################
# MAIN EXECUTION SECTION
#####################################################
def main():
    """
    Main function to execute the script and perform various weather-related database queries and display results.

    This function performs the following tasks:
    1. Connects to the SQLite database.
    2. Displays lists of countries and cities stored in the database.
    3. Allows the user to input a city ID and year, and then retrieves and displays the average annual temperature for the specified city and year.
    4. Allows the user to input a city ID and start date, and then retrieves and displays the average seven-day precipitation for the specified city and starting date.
    5. Allows the user to input a date range, and then retrieves and displays the average mean temperature by city for the specified date range.
    6. Allows the user to input a year, and then retrieves and displays the average annual precipitation by country for the specified year.
    7. Handles user input, validates the input values, and displays error messages when necessary.
    8. Completes all queries and displays the results.

    Raises:
        ValueError: If the user enters an invalid city ID or year.
        sqlite3.OperationalError: If there are issues with database operations or data retrieval.
        Exception: If any unexpected error occurs during execution.

    Prints:
        - Status messages indicating the progress of each query.
        - Query results such as temperature and precipitation data for cities and countries.
        - Error messages for invalid input or database retrieval issues.
    """

    # Change the CWD to the path where this script is located
    change_to_script_directory()
    connection = db_connection("db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db")

    if not connection:
        print("Failed to connect to the database.")
        return

    print()

    # THE LIST OF THE COUNTRIES IN THE DATABASE
    print("THE LIST OF THE COUNTRIES IN THE DATABASE")
    print("select_all_countries(connection)\n")
    countries_table = select_all_countries(connection)
    for row in countries_table:  # Iterate over the data stored in countries_table and display the results.
        print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    print("\n")

    # THE LIST OF THE CITIES IN THE DATABASE
    print("THE LIST OF THE CITIES IN THE DATABASE")
    print("select_all_cities(connection)\n")
    cities_table = select_all_cities(connection)
    for row in cities_table:  # Iterate over the data stored in cities_table and display the results.
        print(f"City Id: {row['id']} -- City Name: {row['name']} -- City Longitude: {row['longitude']} -- "
              f"City Latitude: {row['latitude']} -- Country ID: {row['country_id']}")

    print("\n")

    # THE AVERAGE ANNUAL TEMPERATURE FOR THE SELECTED CITY AND YEAR
    print("THE AVERAGE ANNUAL TEMPERATURE FOR THE SELECTED CITY AND YEAR")
    print("average_annual_temperature(connection, city_id, year)\n")
    display_available_cities(connection)

    city_id_r, city_name_r = extract_cities(connection)
    distinct_years = db_distinct_years(connection)

    while True:
        try:
            city_id_input = input("Enter the City ID: ")
            if not city_id_input.isdigit():
                print("Enter a valid numeric City ID.")
                continue

            city_id = int(city_id_input)
            city_valid, city_message = validate_city_id(city_id, city_id_r)
            if not city_valid:
                print(city_message)
                continue

            year = input(f"Enter the Year (YYYY) from the available years {', '.join(distinct_years)}: ")
            year_valid, year_message = validate_year(year, distinct_years)
            if not year_valid:
                print(year_message)
                continue
            # Retrieve and display temperature records
            temperature_records = average_annual_temperature(connection, city_id, year)
            if temperature_records is None:
                print("Failed to retrieve data from the database.")
                break
            records_found = False
            for record in temperature_records:
                print(f"City Id: {record['city_id']} -- City Name: {record['city_name']} -- Year: {record['year']} -- "
                      f"Annual Mean Temperature: {record['annual_mean_temperature']:.2f}°C")
                records_found = True
            if not records_found:
                print("No data found for the specified city and year.")
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the City ID.")
        except sqlite3.OperationalError as ex:
            print(f"An error occurred while retrieving data: {ex}")

    print("\n")

    # THE AVERAGE SEVEN DAY PRECIPITATION FOR THE SELECTED CITY AND STARTING DATE
    print("THE AVERAGE SEVEN DAY PRECIPITATION FOR THE SELECTED CITY AND STARTING DATE")
    print("average_seven_day_precipitation(connection, city_id, start_date)\n")
    # Display available cities and get city IDs
    display_available_cities(connection)
    city_ids, city_names = extract_cities(connection)

    # Validate city ID
    while True:
        city_id_input = input(f"Enter the city ID from the available options ({', '.join(map(str, city_ids))}): ")

        # Check if the input can be converted to an integer
        if not city_id_input.isdigit():
            print(f"Invalid input: {city_id_input}. Please enter a valid number.")
            continue

        city_valid, city_message = validate_city_id(int(city_id_input), city_ids)
        if not city_valid:
            print(city_message)
        else:
            break

    # Retrieve available dates from the database
    available_dates = select_dates(connection)
    if not available_dates:
        print("No available dates found in the database.")
        return

    print(f"Available date range: {min(available_dates)} - {max(available_dates)}")

    # Validate start date
    while True:
        start_date = input("Enter the start date in YYYY-MM-DD format for the seven-day precipitation: ")
        date_valid, date_message = validate_db_dates(start_date, start_date, available_dates)
        if not date_valid:
            print(date_message)
        else:
            break

    precipitation_records = average_seven_day_precipitation(connection, city_id, start_date)
    # Iterate over the results and display the results.
    for record in precipitation_records:
        print(f"City Id: {record['city_id']} -- City Name: {record['city_name']} -- Seven Days Starting From: {record['start_date']} -- "
              f"Average Seven Day Precipitation: {record['average_seven_day_precipitation']:.2f}mm")

    print("\n")

    # THE AVERAGE MEAN TEMPERATURE BY CITY FOR THE SELECTED RANGE OF DATES
    print("THE AVERAGE MEAN TEMPERATURE BY CITY FOR THE SELECTED RANGE OF DATES")
    print("average_mean_temp_by_city(connection, date_from, date_to)\n")
    available_dates = select_dates(connection)
    if not available_dates:
        print("No available dates found in the database.")
        return

    print(f"Available date range: {min(available_dates)} - {max(available_dates)}")
    while True:
        date_from, date_to = get_date_input()
        dates_valid, error_message = validate_db_dates(date_from, date_to, available_dates)
        if dates_valid:
            break
        print(error_message)

    city_temperature_records = average_mean_temp_by_city(connection, date_from, date_to)
    if city_temperature_records is not None:

        for record in city_temperature_records:  # Iterate over city_temperature_records to display the results.
            print(f"City Id: {record['city_id']} -- City Name: {record['city_name']} -- Date From: {date_from} -- "
                  f"Date To: {date_to} -- Average Mean Temperature: {record['average_mean_temperature']:.2f}°C")

    print("\n")

    # THE AVERAGE ANNUAL PRECIPITATION BY COUNTRY FOR THE SELECTED YEAR
    print("THE AVERAGE ANNUAL PRECIPITATION BY COUNTRY FOR THE SELECTED YEAR")
    print("average_annual_precipitation_by_country(connection, year)\n")
    distinct_years = db_distinct_years(connection)
    # Display available years to the user
    print(f"Available years: {', '.join(distinct_years)}")
    while True:
        try:
            # Prompt for the year and validate it
            year = input(f"Enter the Year (YYYY) {', '.join(distinct_years)}: ")
            year_valid, year_message = validate_year(year, distinct_years)
            if not year_valid:
                print(year_message)
                continue

            country_precipitation_records = average_annual_precipitation_by_country(connection, year)  # Retrieve precipitation records

            has_results = False  # Check if results are valid
            if country_precipitation_records:
                for record in country_precipitation_records:
                    has_results = True
                    print(f"Country Id: {record['id']} -- Country Name: {record['name']} -- Year: {record['year']} -- "
                          f"Average Annual Precipitation: {record['average_annual_precipitation']:.2f}mm")

            if not has_results:
                print(f"No precipitation data found for the year {year}.")
            break  # Exit the loop on successful execution
        except sqlite3.OperationalError as ex:
            print(f"An error occurred while retrieving data: {ex}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    print("\nExecution completed!. \nAll the query functions have been executed!! \nKindly check the plots in phase 2!!!\n")


if __name__ == "__main__":
    main()
