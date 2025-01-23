# Author: <Olawale Francis Onaolapo>
# 

##############################################################################
# IMPORTED LIBRARIES - FOR PLOTS
##############################################################################
import os
import phase_1 as fp1  # IMPORTED MODULE FROM THE PHASE 1 OF THIS ICA
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backend_bases import MouseButton
from phase_1 import (
    extract_cities,
    display_available_cities,
    db_distinct_years,
    get_date_input,
    select_dates,
    validate_db_dates,
    validate_city_id,
    validate_user_inputs,
    )


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
# FUNCTION FOR CONNECTING TO THE DATABASE - IN USE BY ALL THE PLOTS
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


#########################################################################
# PLOT 1 - GROUP BAR CHART PLOTTING FUNCTIONS - ANNUAL TEMPERATURE
#########################################################################

# DB_DISTINCT_YEARS FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 1

# EXTRACT_CITIES FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 1

def calculate_annual_temperatures(connection, city_ids, years):
    """Calculate average annual temperature for each city and year."""
    records = {"city_ids": [], "years": [], "city_annual_temperature": []}
    for city_id in city_ids:
        for year in years:
            avg_annual_mean = fp1.average_annual_temperature(connection, city_id, year)
            for avg_mean in avg_annual_mean:
                records["city_ids"].append(city_id)
                records["years"].append(year)
                records["city_annual_temperature"].append(round(avg_mean['annual_mean_temperature'], 2))
    return records


def plot_annual_temperatures_grouped_bar(city_names, city_annual_temperature_record):
    """Plot average annual temperatures as a grouped bar chart."""
    unique_city_ids_set = set(city_annual_temperature_record["city_ids"])
    unique_city_ids = sorted(unique_city_ids_set)

    city_positions = list(range(len(unique_city_ids)))
    width = 0.17

    years_set = sorted(set(city_annual_temperature_record["years"]))
    num_years = len(years_set)

    color_map = plt.get_cmap('Pastel2', num_years)
    colors = []
    for bar_year in range(num_years):
        colors.append(color_map(bar_year))
    labels = []
    for year in years_set:
        labels.append(f'Year {year}')

    temperatures = []
    for nyear in range(num_years):
        temp = []
        for t in range(nyear, len(city_annual_temperature_record['city_annual_temperature']), num_years):
            temp.append(city_annual_temperature_record['city_annual_temperature'][t])
        temperatures.append(temp)

    fig, ax = plt.subplots(figsize=(10, 6))
    for nyear in range(len(temperatures)):
        temp = temperatures[nyear]
        positions = []
        for pos in city_positions:
            adjusted_position = pos + (nyear - (num_years - 1) / 2) * width
            positions.append(adjusted_position)
        bars = ax.bar(positions, temp, width, label=labels[nyear], color=colors[nyear])

        for bar, temperature, year in zip(bars, temp, [years_set[nyear]] * len(temp)):
            height = bar.get_height()
            if height:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f'({year})',
                    ha='center',
                    va='center',
                    rotation=90,
                    fontsize=8,
                    color='black'
                )
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 1.5,
                    f'({temperature:.1f}°C)',
                    ha='center',
                    va='bottom',
                    rotation=90,
                    fontsize=8,
                    color='black'
                )

    ax.set_xlabel('City Name', fontsize=12)
    ax.set_ylabel('Average Annual Mean Temperature (°C)', fontsize=12)
    ax.set_title(f'Annual Mean Temperature by City and Year\n({years_set[0]} to {years_set[-1]})', fontsize=16)
    ax.set_xticks(city_positions)
    ax.set_xticklabels(city_names, rotation=45, ha='right')
    ax.legend(title='Year', fontsize=10)

    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


#########################################################################
# PLOT 2 - BAR CHART PLOTTING FUNCTIONS - TEMPERATURE BETWEEN DATE RANGE
#########################################################################

# GET_DATE_INPUT FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 2

# VALIDATE_DB_DATES FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 2


def get_mean_temperature_data(connection, date_from, date_to):
    """
    Retrieves mean temperature data for the specified date range using phase_1's function.
    Returns:
        list: A list of tuples containing average mean temperature and city name.
    """
    result = []
    for item in fp1.average_mean_temp_by_city(connection, date_from, date_to):
        result.append((item['average_mean_temperature'], item['city_name']))
    return result


def process_mean_temperature_data(mean_temperature_record):
    """
    Processes the raw mean temperature data into a formatted dictionary.
    Args:
        mean_temperature_record (list): A list of tuples (average_mean_temperature, city_name).
    Returns:
        dict: A dictionary with keys "city_names" and "average_mean_temperatures".
    """
    processed_data = {
        "city_names": [],
        "average_mean_temperatures": [],
    }
    for average_mean_temperature, city_name in mean_temperature_record:
        processed_data["average_mean_temperatures"].append(round(average_mean_temperature, 2))
        processed_data["city_names"].append(city_name)
    return processed_data


def calculate_mean_temperature(temperatures):
    """
    Calculates the mean of a list of temperatures.
    Args:
        temperatures (list): List of temperature values.
    Returns:
        float: Mean temperature rounded to 2 decimal place.
    """
    if not temperatures:
        return 0
    return round(sum(temperatures) / len(temperatures), 2)


def plot_bar_chart_with_mean(data, mean_temperature, date_from, date_to):
    """
    Plots a bar chart of the average mean temperature by city and adds a horizontal line
    for the overall mean temperature.
    Args:
        data (dict): Dictionary containing "city_names" and "average_mean_temperatures".
        mean_temperature (float): Overall mean temperature for all cities.
        date_from (str): Start date of the data range.
        date_to (str): End date of the data range.
    """
    fig, ax = plt.subplots()
    bars = ax.bar(
        range(len(data["city_names"])),
        data["average_mean_temperatures"],
        color="tan",
        label="City Average Temperatures (°C)"
    )

    ax.axhline(y=mean_temperature, color="red", linestyle="--", linewidth=2, label=f"Mean Temperature ({mean_temperature}°C)")

    ax.set_xlabel("Cities")
    ax.set_ylabel("Average Mean Temperature (°C)")
    ax.set_title(f"Average Mean Temperature by City from {date_from} to {date_to}")
    ax.set_xticks(range(len(data["city_names"])))
    ax.set_xticklabels(data["city_names"], rotation=45, ha="right")

    for bar, temp in zip(bars, data["average_mean_temperatures"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{temp}°C",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.legend()
    plt.tight_layout()
    plt.show()


#########################################################################
# PLOT 3 - BAR CHART PLOTTING FUNCTIONS - 7 DAYS TEMPERATURE
#########################################################################
def get_date_range(connection):
    """
    Prompts the user for a start date and calculates the end date.

    Args:
        connection: SQLite database connection object.

    Returns:
        tuple: (start_date, end_date)
    """
    while True:
        start_date = input("Please, specify the start date (YYYY-MM-DD): ")
        if len(start_date) == 10 and start_date[4] == "-" and start_date[7] == "-":
            try:
                cursor = connection.cursor()
                new_date = cursor.execute("SELECT date(?, '+6 days') AS end_date", (start_date,))
                for row in new_date:
                    end_date = row["end_date"]
                    return start_date, end_date 
            except Exception as ex:
                print(f"Error calculating end date: {ex}")
                return None, None
        print("Invalid date format. Please use YYYY-MM-DD.")

# EXTRACT_CITIES FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 3


def get_precipitation_averages(connection, city_ids, start_date):
    """
    Retrieves the average 7-day precipitation for a list of cities starting from a given date.

    Args:
        connection: SQLite database connection object.
        city_ids (list): List of city IDs to retrieve precipitation data for.
        start_date (str): Start date (YYYY-MM-DD) for the 7-day period.

    Returns:
        tuple: (city_names, precipitation_averages)
            city_names: List of city names.
            precipitation_averages: List of average precipitation values for each city.
    """
    city_names = []
    precipitation_averages = []

    for city_id in city_ids:
        results = fp1.average_seven_day_precipitation(connection, city_id, start_date)

        for row in results:
            city_names.append(row["city_name"])
            precipitation_averages.append(row["average_seven_day_precipitation"])

    return city_names, precipitation_averages


def plot_seven_day_precipitation_chart(city_names, precipitation_averages, start_date, end_date):
    """
    Plots a bar chart of average precipitation for the past 7 days and a mean line.

    Args:
        city_names (list): List of city names.
        precipitation_averages (list): List of average precipitation values.
        start_date (str): Start date of the 7-day period.
        end_date (str): End date of the 7-day period.
    """
    if not city_names or not precipitation_averages:
        print(f"No precipitation data available for the specified date range: {start_date} - {end_date}.")
        return

    mean_precipitation = sum(precipitation_averages) / len(precipitation_averages)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        city_names,
        precipitation_averages,
        color="skyblue",
        label="7 days Average Precipitation per City"
    )

    plt.axhline(
        y=mean_precipitation,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"7 days Mean Precipitation (All cities): ({mean_precipitation:.2f}mm)"
    )

    plt.xlabel("City Names", fontsize=12)
    plt.ylabel("Average Precipitation (mm)", fontsize=12)
    plt.title(f"7-Day Average Precipitation by City\n({start_date} to {end_date})", fontsize=14)
    plt.xticks(rotation=45, ha="right")

    for bar, avg_precipitation in zip(bars, precipitation_averages):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{avg_precipitation:.2f}mm",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.legend()
    plt.grid(axis='y', linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


#########################################################################
# PLOT 4 - HISTOGRAM CHART PLOTTING FUNCTIONS - PRECIPITATION
#########################################################################

# DISPLAY_AVAILABLE_CITIES FROM PHASE 1 IS USED IN THIS PLOT 4

# GET_DATE_INPUT FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 4


def temp_n_prep_by_city(connection, city_id, date_from, date_to):
    """
    Gets temperature and precipitation data for a specific city within a specified date range.
    """
    try:
        query = """
            SELECT dw.mean_temp AS mean_temperature,
                   dw.min_temp AS min_temperature,
                   dw.max_temp AS max_temperature,
                   dw.precipitation AS precipitation,
                   dw.date AS date
            FROM [daily_weather_entries] AS dw
            WHERE dw.city_id = ?
              AND dw.date >= ?
              AND dw.date <= ?
            ORDER BY dw.date
        """
        cursor = connection.cursor()
        results = cursor.execute(query, (city_id, date_from, date_to))

        data = []
        for row in results:
            data.append({
                'date': row['date'],
                'min_temperature': row['min_temperature'],
                'max_temperature': row['max_temperature'],
                'mean_temperature': row['mean_temperature'],
                'precipitation': row['precipitation']
            })
        return data
    except sqlite3.OperationalError as ex:
        print("Database error:", ex)
        return []


def plot_precipitation_histogram(city_name, data, start_date, end_date):
    """
    Plots a histogram of precipitation data for a specific city,
    including a vertical line for the average precipitation.
    """
    if not data:
        print(f"No data available for {city_name} in the specified date range.")
        return

    precipitations = []
    for row in data:
        precipitations.append(row['precipitation'])

    if not precipitations:
        print(f"No precipitation data available for {city_name}.")
        return

    avg_precipitation = sum(precipitations) / len(precipitations)

    plt.figure(figsize=(10, 6))
    plt.hist(precipitations, bins=20, color='green', alpha=0.7)
    plt.axvline(x=avg_precipitation, color='red', linestyle='--', linewidth=2, label=f"({start_date} to {end_date})\nAverage precipitation: {avg_precipitation:.2f}mm")
    plt.title(f"Precipitation Distribution - {city_name}\n({start_date} to {end_date})")
    plt.xlabel("Precipitation (mm)")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()


###############################################################################
# PLOT 5 - SCATTER PLOT CHART PLOTTING FUNCTIONS - TEMPERATURE & PRECIPITATION
###############################################################################

# DISPLAY_AVAILABLE_CITIES FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 5

# GET_DATE_INPUT FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 5

# TEMP_N_PREP_BY_CITY FUNCTION FROM PLOT 4 IS USED IN THIS PLOT 5

def plot_scatter_plot(city_name, data, start_date, end_date):
    """
    Plots a scatter plot of mean_temperature against precipitation for a specific city.
    """
    if not data:
        print(f"No data available for {city_name} in the specified date range.")
        return

    mean_temps = []
    precipitations = []

    for row in data:
        mean_temps.append(row['mean_temperature'])
        precipitations.append(row['precipitation'])

    plt.figure(figsize=(10, 6))
    plt.scatter(mean_temps, precipitations, color='purple', alpha=0.6)
    plt.title(f"Mean Temperature vs Precipitation - {city_name}\n({start_date} to {end_date})")
    plt.xlabel("Mean Temperature (°C)")
    plt.ylabel("Precipitation (mm)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


###############################################################################
# PLOT 6 - LINE CHART PLOTTING FUNCTIONS - TEMPERATURE
###############################################################################

# DISPLAY_AVAILABLE_CITIES FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 6

# GET_DATE_INPUT FUNCTION FROM PHASE 1 IS USED IN THIS PLOT 6

# TEMP_N_PREP_BY_CITY FUNCTION FROM PLOT 4 IS USED IN THIS PLOT 6


def plot_temperature_line_chart(city_name, data, start_date, end_date):
    """
    Plots temperature data dynamically for the entire input date range,
    with horizontal and vertical sliders and dragging functionality.
    """
    if not data:
        print(f"No data available for {city_name} in the specified date range.")
        return

    dates = []
    for row in data:
        dates.append(row['date'])

    min_temps = []
    for row in data:
        min_temps.append(row['min_temperature'])

    max_temps = []
    for row in data:
        max_temps.append(row['max_temperature'])

    mean_temps = []
    for row in data:
        mean_temps.append(row['mean_temperature'])

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.3, left=0.2)

    line_min, = ax.plot(dates, min_temps, label="Min Temp", color='blue', marker='.')
    line_max, = ax.plot(dates, max_temps, label="Max Temp", color='red', marker='.')
    line_mean, = ax.plot(dates, mean_temps, label="Mean Temp", color='green', marker='.')

    ax.set_title(f"Temperature Trends - {city_name}\n({start_date} to {end_date})")
    ax.set_xlabel(f"Date: from {start_date} to {end_date}", labelpad=10)
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    ax.set_xlim(dates[0], dates[min(14, len(dates)) - 1])
    ax.set_xticks(dates[:14])
    ax.set_xticklabels(dates[:14], rotation=45)

    ax.set_ylim(min(min_temps) - 5, max(max_temps) + 5)

    ax_slider_x = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor='lightgrey')
    slider_x = Slider(ax_slider_x, 'Horizontal Frame', 0, len(dates) - 14, valinit=0, valstep=1)

    ax_slider_y = plt.axes([0.05, 0.25, 0.03, 0.5], facecolor='lightgrey')
    slider_y = Slider(ax_slider_y, 'Vertical Frame', min(min_temps) - 5, max(max_temps) + 5, valinit=0, orientation='vertical')

    ax_slider_y.set_ylabel("Vertical Frame", labelpad=15, rotation=270)

    def update(val):
        frame_x = int(slider_x.val)
        frame_x_end = min(frame_x + 14, len(dates))
        ax.set_xlim(dates[frame_x], dates[frame_x_end - 1])
        ax.set_xticks(dates[frame_x:frame_x_end])
        ax.set_xticklabels(dates[frame_x:frame_x_end], rotation=45)

        frame_y = slider_y.val
        ax.set_ylim(frame_y, max(max_temps) + 5)

        fig.canvas.draw_idle()

    slider_x.on_changed(update)
    slider_y.on_changed(update)

    dragging = False
    offset_x = 0
    offset_y = 0

    def on_press(event):
        nonlocal dragging, offset_x, offset_y
        if event.inaxes != ax or event.button != MouseButton.LEFT:
            return
        dragging = True
        offset_x = event.xdata
        offset_y = event.ydata

    def on_release(event):
        nonlocal dragging
        dragging = False

    def on_motion(event):
        nonlocal dragging, offset_x, offset_y
        if not dragging or event.inaxes != ax:
            return
        dx = event.xdata - offset_x
        dy = event.ydata - offset_y
        ax.set_xlim(ax.get_xlim()[0] - dx, ax.get_xlim()[1] - dx)
        ax.set_ylim(ax.get_ylim()[0] - dy, ax.get_ylim()[1] - dy)
        offset_x = event.xdata
        offset_y = event.ydata
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('button_release_event', on_release)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)

    plt.show()


###############################################################################
# SUPPORT FUNCTION FOR PLOTTING PLOT 4, PLOT 5 AND PLOT 6
###############################################################################
def prepare_and_plot_chart(connection, plot_function):
    """
    Prepare the data and call a provided plotting function to generate the chart.

    Args:
        connection: The database connection object.
        plot_function: A function that takes (city_name, city_weather_records, date_from, date_to)
                       as arguments and handles the plotting logic.

    Returns:
        None
    """
    display_available_cities(connection)
    city_id_r, city_name_r = extract_cities(connection)

    while True:
        try:
            while True:
                city_id_input = input("Enter the City ID (or press 'c' to cancel): ")

                if city_id_input.lower() == 'c':
                    print("Operation cancelled.")
                    return

                if not city_id_input.isdigit():
                    print("Enter a valid numeric City ID.")
                    continue

                city_id = int(city_id_input)
                city_valid, city_message = validate_city_id(city_id, city_id_r)
                if city_valid:
                    break
                else:
                    print(city_message)

            available_dates = select_dates(connection)
            if not available_dates:
                print("No available dates found in the database.")
                return

            print(f"Available date range: {min(available_dates)} - {max(available_dates)}")

            while True:
                date_from, date_to = get_date_input()

                valid, error_message = validate_user_inputs(connection, date_from, date_to, city_id)
                if valid:
                    break
                else:
                    print(error_message)
                    cancel = input("Press 'c' to cancel or any other key to try again: ")
                    if cancel.lower() == 'c':
                        print("Operation cancelled.")
                        return

            city_weather_records = temp_n_prep_by_city(connection, city_id, date_from, date_to)

            city_name = None
            for row in fp1.select_all_cities(connection):
                if row['id'] == city_id:
                    city_name = row['name']
                    break

            if city_name:
                # Use the provided plot function to plot the chart
                plot_function(city_name, city_weather_records, date_from, date_to)
            else:
                print("City not found.")
            break

        except ValueError:
            print("Invalid input. Please enter a numeric value for the City ID.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


#################################################################
# PLOT EXECUTION SECTION - REFERENCED AS MAIN
#################################################################
def main():
    """
    Main function to execute the script and generate various weather-related plots from the database data.

    The function performs the following tasks:
    1. Sets the working directory and establishes a connection to the SQLite database.
    2. Executes a sequence of plotting tasks:
        - Plot 1: Annual mean temperature by city and year using a grouped bar chart.
        - Plot 2: Average mean temperature by city for a specified date range using a bar chart.
        - Plot 3: Precipitation chart for a seven-day date range using a bar chart.
        - Plot 4: Precipitation chart by city for a specified date range using a histogram.
        - Plot 5: Temperature and precipitation chart for a specified date range using a scatter plot.
        - Plot 6: Temperature trend for a specified date range using line charts.
    3. Handles user inputs for date ranges, validates the input, and retrieves necessary weather data.
    4. Plots the data using various visualizations such as bar charts, histograms, scatter plots, and line charts.

    Raises:
        ValueError: If invalid date ranges are entered or if data retrieval fails.
        Exception: If an unexpected error occurs during the plotting or database operations.

    Prints:
        - Status messages regarding the progress of each plot.
        - Error messages for failed database connections or invalid date input.
    """

    # WORKING DIRECTORY AND DATABASE CONNECTION
    change_to_script_directory()
    connection = db_connection("db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db")

    if not connection:
        print("Failed to connect to the database.")
        return

    # PLOT 1: PLOT ANNUAL MEAN TEMPERATURE BY CITY AND YEAR USING GROUPED BAR CHART
    print("PLOT 1: PLOT ANNUAL MEAN TEMPERATURE BY CITY AND YEAR USING GROUPED BAR CHART")
    print("plot_annual_temperatures_grouped_bar(db_city_names, city_annual_temperature_record)\n")

    db_years = db_distinct_years(connection)
    db_city_ids, db_city_names = extract_cities(connection)
    city_annual_temperature_record = calculate_annual_temperatures(connection, db_city_ids, db_years)
    plot_annual_temperatures_grouped_bar(db_city_names, city_annual_temperature_record)

    print("\n")

    # PLOT 2: PLOT AVERAGE MEAN TEMPERATURE BY CITY FOR A SPECIFIED DATE RANGE USING BAR CHART
    print("PLOT 2: PLOT AVERAGE MEAN TEMPERATURE BY CITY FOR A SPECIFIED DATE RANGE USING BAR CHART")
    print("plot_bar_chart_with_mean(data, mean_temperature, date_from, date_to)\n")

    # Retrieve and validate available dates
    available_dates = select_dates(connection)
    if not available_dates:
        print("No available dates found in the database.")
        return

    print(f"Available date range: {min(available_dates)} - {max(available_dates)}")

    while True:
        date_from, date_to = get_date_input()
        is_valid, error_message = validate_db_dates(date_from, date_to, available_dates)
        if not is_valid:
            print(error_message)
            continue
        break

    # Retrieve, process and plot the temperature data
    mean_temperature_record = get_mean_temperature_data(connection, date_from, date_to)
    if not mean_temperature_record:
        print(f"No data available for the selected date range: {date_from} - {date_to}.")
        return

    data = process_mean_temperature_data(mean_temperature_record)
    mean_temperature = calculate_mean_temperature(data["average_mean_temperatures"])

    plot_bar_chart_with_mean(data, mean_temperature, date_from, date_to)

    print("\n")

    # PLOT 3: PLOT PRECIPITATION CHART FOR SEVEN DAYS DATE RANGE USING BAR CHART
    print("PLOT 3: PLOT PRECIPITATION CHART FOR SEVEN DAYS DATE RANGE USING BAR CHART")
    print("plot_seven_day_precipitation_chart(city_names, precipitation_averages, start_date, end_date)")
    print("The end_date will be automatically calculated as the next 6 days from the start_date\n")

    available_dates = select_dates(connection)
    if not available_dates:
        print("No available dates found in the database.")
        return

    print(f"Available date range: {min(available_dates)} - {max(available_dates)}")

    while True:
        start_date, end_date = get_date_range(connection)
        is_valid, error_message = validate_db_dates(start_date, end_date, available_dates)
        if not is_valid:
            print(error_message)
            continue
        break
    db_city_ids, db_city_names = extract_cities(connection)
    city_names, precipitation_averages = get_precipitation_averages(connection, db_city_ids, start_date)
    plot_seven_day_precipitation_chart(city_names, precipitation_averages, start_date, end_date)

    print("\n")

    # PLOT 4: PLOT PRECIPITATION CHART BY CITY FOR A SPECIFIED DATE RANGE USING HISTOGRAM
    print("PLOT 4: PLOT PRECIPITATION CHART BY CITY FOR A SPECIFIED DATE RANGE USING HISTOGRAM")
    print("plot_precipitation_histogram(city_name, city_weather_records, date_from, date_to)\n")
    prepare_and_plot_chart(connection, plot_precipitation_histogram)

    print("\n")

    # PLOT 5: PLOT TEMPERATURE AND PRECIPITATION CHART FOR A SPECIFIED DATE RANGE USING SCATTER PLOT
    print("PLOT 5: PLOT TEMPERATURE AND PRECIPITATION CHART FOR A SPECIFIED DATE RANGE USING SCATTER PLOT")
    print("plot_scatter_plot(city_name, city_weather_records, date_from, date_to)\n")
    prepare_and_plot_chart(connection, plot_scatter_plot)

    print("\n")

    # PLOT 6: PLOT TEMPERATURE TREND FOR A SPECIFIED DATE RANGE USING LINE CHARTS
    print("PLOT 6: PLOT TEMPERATURE TREND FOR A SPECIFIED DATE RANGE USING LINE CHARTS")
    print("plot_temperature_line_chart(city_name, city_weather_records, date_from, date_to)\n")
    prepare_and_plot_chart(connection, plot_temperature_line_chart)

    print()
    print("THE FINAL CHART IN PHASE 2 HAS BEEN PLOTTED. THANK YOU FOR REVIEWING THE SEQUENCE OF PLOTS")
    print()
    print("KINDLY REVIEW PHASES 3 AND 4 FOR THE WEATHER API DATA REQUESTING APPLICATION")
    print()


if __name__ == "__main__":
    main()
