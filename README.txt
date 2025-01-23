THIS IS THE DESCRIPTION OF HOW TO RUN THE PROGRAMS, INCLUDING THE DETAILS OF THE COMMAND LINE ARGUMENTS AND ANY DEPENDENCY INFORMATION

ROOT FOLDER DESCRIPTION: The root folder contains the following:
	- Python scripts written with Visual Studio Code named phase_1, phase_2, phase_3 and phase_4. These are the developed programs that needs to be examined by you. The description of how to run and test the Python scripts can be found below.
	- Standalone application created with thinter and pyinstaller. This is the standalone application developed for doing the programs done by both phase_3 and phase_4 Python scripts. The description of how to run and test the application can be found below.
	- db folder, which contains the SQLite database used for testing the application and the Python scripts above. It is important to leave the folder in the same location as the Python scripts and the standalone application, as it is submitted.
	- Report folder, which contains the report submitted in compliance with the project requirement and it also contains the blackbox testing entries for the programs.
	- _pycache_ folder, build folder and dist folder, which were created automatically when the phase 4 standalone application was build with the pyinstaller package. There is no need for you to use these folder during the running and testing of the application. You should just leave the folders as they are.
	- The items labelled tempCodeRunnerFile and phase_4.spec should also be left as they are. There is no need for you to use these items during the running and testing of the application.


HOW TO RUN THE PROGRAMS, INCLUDING THE DETAILS OF THE COMMAND LINE ARGUMENTS AND ANY DEPENDENCY INFORMATION

PHASE 1 - DATABASE QUERY FUNCTIONS

DEPENDENCY INFORMATION: The dependencies required to run the phase 1 program are os and sqlite3 modules. Both modules are Python in-built modules.

The path directory is set with the os module to guide the Visual Studio code, used for writing this program, to execute the code with its starting working directory as the location of the Python script while the sqlite3 module is important to interact with the SQLite database.

There are six functions in phase 1 of the ICA that were executed in the main function to query the database.

A single connection to the database is done for all the functions to use. 

The variable name for the connection is: connection

Each of the functions can be executed as shown below:


FUNCTION 1: select_all_countries(connection)

STEP 1: Click the run code button of the Visual Studio code. This function do not require any user input.
	
STEP 2: Output Example: Country Id: 1 -- Country Name: Great Britain -- Country Timezone: Europe/London
			Country Id: 2 -- Country Name: France -- Country Timezone: Europe/Berlin
			Country Id: 3 -- Country Name: Nigeria -- Country Timezone: Africa/Lagos


FUNCTION 2: select_all_cities(connection)

STEP 1: The Visual Studio code clicked run code button from function 1 will execute this function 2 automatically. This function do not require any user input.
	
STEP 2: Output Example: City Id: 1 -- City Name: Middlesbrough -- City Longitude: -1.2344047 -- City Latitude: 54.5760419 -- Country ID: 1
			City Id: 2 -- City Name: London -- City Longitude: -0.144055084527687 -- City Latitude: 51.4893335 -- Country ID: 1
			City Id: 3 -- City Name: Paris -- City Longitude: 2.3483915 -- City Latitude: 48.8534951 -- Country ID: 2
			City Id: 4 -- City Name: Toulouse -- City Longitude: 1.4442469 -- City Latitude: 43.6044622 -- Country ID: 2
			City Id: 5 -- City Name: Lagos -- City Longitude: 3.3941795 -- City Latitude: 6.4550575 -- Country ID: 3
			City Id: 6 -- City Name: Leeds -- City Longitude: -1.5437941 -- City Latitude: 53.7974185 -- Country ID: 1


FUNCTION 3: average_annual_temperature(connection, city_id, year)

STEP 1: The Visual Studio code clicked run code button from function 1 will start the execution of this function 3 automatically. 

STEP 2: Enter the city ID between 1 to 6
	Example: Enter the City ID: 2

STEP 3: Enter the Year (YYYY) from the available years 2020, 2021, 2022, 2023, 2024:
	Example: Enter the Year (YYYY) from the available years 2020, 2021, 2022, 2023, 2024: 2020
	
STEP 4: Output Example: City Id: 2 -- City Name: London -- Year: 2020 -- Annual Mean Temperature: 11.57°C
	

FUNCTION 4: average_seven_day_precipitation(connection, city_id, start_date)

STEP 1: The Visual Studio code clicked run code button from function 1 will start the execution of this function 4 automatically after the completion of function 3. 

STEP 2: Enter the city ID from the available options (1, 2, 3, 4, 5, 6):
	Example: Enter the City ID: 2

STEP 3: Enter the Year (YYYY) from the available years 2020, 2021, 2022, 2023, 2024:
	Example: Enter the city ID from the available options (1, 2, 3, 4, 5, 6): 3
	
STEP 4: Enter the start date in YYYY-MM-DD format for the seven-day precipitation:
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Enter the start date in YYYY-MM-DD format for the seven-day precipitation: 2020-09-09

STEP 5: Output Example: City Id: 2 -- City Name: London -- Seven Days Starting From: 2020-09-09 -- Average Seven Day Precipitation: 0.00mm


FUNCTION 5: average_mean_temp_by_city(connection, date_from, date_to)

STEP 1: The Visual Studio code clicked run code button from function 1 will start the execution of this function 5 automatically after the completion of function 4. 

STEP 2: Please, specify the start date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the start date in YYYY-MM-DD format: 2020-02-02

STEP 3: Please, specify the end date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the end date in YYYY-MM-DD format: 2023-01-02
	
STEP 4: Output Example: City Id: 1 -- City Name: Middlesbrough -- Date From: 2020-02-02 -- Date To: 2023-01-02 -- Average Mean Temperature: 10.41°C
			City Id: 2 -- City Name: London -- Date From: 2020-02-02 -- Date To: 2023-01-02 -- Average Mean Temperature: 11.53°C
			City Id: 3 -- City Name: Paris -- Date From: 2020-02-02 -- Date To: 2023-01-02 -- Average Mean Temperature: 12.81°C
			City Id: 4 -- City Name: Toulouse -- Date From: 2020-02-02 -- Date To: 2023-01-02 -- Average Mean Temperature: 15.20°C
			City Id: 5 -- City Name: Lagos -- Date From: 2020-02-02 -- Date To: 2023-01-02 -- Average Mean Temperature: 26.98°C
			City Id: 6 -- City Name: Leeds -- Date From: 2020-02-02 -- Date To: 2023-01-02 -- Average Mean Temperature: 10.35°C


FUNCTION 6: average_annual_precipitation_by_country(connection, year)

STEP 1: The Visual Studio code clicked run code button from function 1 will start the execution of this function 6 automatically after the completion of function 5.

STEP 2: Enter the Year (YYYY) 2020, 2021, 2022, 2023, 2024:
	Choose from the available years in the submitted database: 2020, 2021, 2022, 2023, 2024
	Example: Enter the Year (YYYY) 2020, 2021, 2022, 2023, 2024: 2023

STEP 3: Output Example: Country Id: 1 -- Country Name: Great Britain -- Year: 2023 -- Average Annual Precipitation: 2.54mm
			Country Id: 2 -- Country Name: France -- Year: 2023 -- Average Annual Precipitation: 2.50mm
			Country Id: 3 -- Country Name: Nigeria -- Year: 2023 -- Average Annual Precipitation: 3.75mm


NOTE: All the six phase 1 query functions have been completely executed.


PHASE 2 FUNCTIONS
DEPENDENCY INFORMATION: The dependencies required to run the phase 2 program are os module, sqlite3 module, matplotlib module and the phase 1 module of this ICA.

Both os module and sqlite3 module are Python in-built modules.

pip install matplotlib should be used to install matplotlib from the CMD prompt on windows. You can research how to install matplotlib in Python if you are using another operating system.

Ensure the phase 1 Python script (module) is in the same folder directory you are executing this phase 2 Python script from.

There are six plot functions in this phase 2 of the ICA that were executed in the main function to visualize the return from the database of some query functions using various types of charts.


PHASE 2 - FUNCTIONS FOR PLOTTING DATABASE DATA

Note that the path directory, change_to_script_directory() function, is used to guide the Visual Studio code to execute the code with its starting working directory as the current location of the Python script

A single connection to the database, db_connection(connection), is in use by all the plot functions. The variable name for the connection is: connection

Each of the plotted charts can be executed as shown below:


PLOT FUNCTION 1: plot_annual_temperatures_grouped_bar(db_city_names, city_annual_temperature_record)
STEP 1: Click the run code button of the Visual Studio code. This plot function do not require any user input.

STEP 2: Output: A group bar chart of the plot of annual mean temperature by city and year is  displayed for all the 6 cities in the database and the years of records in the database, 2020 -2024.

STEP 3: After completion of the chart review and ready to check the plot function 2, close the image by clicking on the x button on the top-right side of the image.
	

PLOT FUNCTION 2: plot_bar_chart_with_mean(data, mean_temperature, date_from, date_to)
STEP 1: The Visual Studio code clicked run code button from plot function 1 will start the execution of this plot function 2 automatically after the chart image of the plot function 1 is closed.

STEP 2: Please, specify the start date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the start date in YYYY-MM-DD format: 2020-11-02

STEP 3: Please, specify the end date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the end date in YYYY-MM-DD format: 2024-12-12
	
STEP 4: Output Example: A bar chart of average mean temperature by city from 2020-11-02 to 2024-12-12, also showing the mean temperature for the range of dates as a horizontal red dash line.

STEP 5: After completion of the chart review and ready to check the plot function 3, close the image by clicking on the x button on the top-right side of the image.


PLOT FUNCTION 3: plot_seven_day_precipitation_chart(city_names, precipitation_averages, start_date, end_date)
STEP 1: The Visual Studio code clicked run code button from plot function 1 will start the execution of this plot function 3 automatically after the chart image of the plot function 2 is closed.

STEP 2: Please, specify the start date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	The end date for the function input is calculated automatically as the next 6 days from the start date inputted
	Example: Please, specify the start date (YYYY-MM-DD): 2022-01-02

STEP 3: Output Example: A bar chart of the 7-day average precipitation by city from 2022-01-02 to 2022-01-08, also showing the mean precipitation for the 7 days range of dates as a horizontal red dash line.

STEP 4: After completion of the chart review and ready to check the plot function 4, close the image by clicking on the x button on the top-right side of the image.


PLOT FUNCTION 4: plot_precipitation_histogram(city_name, city_weather_records, date_from, date_to)

STEP 1: The Visual Studio code clicked run code button from plot function 1 will start the execution of this plot function 4 automatically after the chart image of the plot function 3 is closed.

STEP 2: Enter the City ID (or press 'c' to cancel): 
	Choose from the available Available Cities in the format: [City ID = City Name]
[1 = Middlesbrough; 2 = London; 3 = Paris; 4 = Toulouse; 5 = Lagos; 6 = Leeds]
	Example: Enter the City ID (or press 'c' to cancel): 2
	Note that the plot function will be terminated and the next plot function, plot function 5, will start running if you press c as an input through-out this plot function 4 program.

STEP 3: Please, specify the start date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the start date in YYYY-MM-DD format: 2020-01-01

STEP 4: Please, specify the end date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the end date in YYYY-MM-DD format: 2023-07-15
	
STEP 5: Output Example: A histogram chart showing the precipitation distribution of London from 2020-01-01 to 2023-07-15, also showing the mean temperature for the range of dates as a vertical red dash line.

STEP 6: After completion of the chart review and ready to check the plot function 5, close the image by clicking on the x button on the top-right side of the image.


PLOT FUNCTION 5: plot_scatter_plot(city_name, city_weather_records, date_from, date_to)

STEP 1: The Visual Studio code clicked run code button from plot function 1 will start the execution of this plot function 5 automatically after the chart image of the plot function 4 is closed.

STEP 2: Enter the City ID (or press 'c' to cancel): 
	Choose from the available Available Cities in the format: [City ID = City Name]
[1 = Middlesbrough; 2 = London; 3 = Paris; 4 = Toulouse; 5 = Lagos; 6 = Leeds]
	Example: Enter the City ID (or press 'c' to cancel): 4
	Note that the plot function will be terminated and the next plot function, plot function 6, will start running if you press c as an input through-out this plot function 5 program.

STEP 3: Please, specify the start date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the start date in YYYY-MM-DD format: 2020-02-10

STEP 4: Please, specify the end date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the end date in YYYY-MM-DD format: 2023-12-30
	
STEP 5: Output Example: A scatter plot chart showing the precipitation versus mean temperature for Toulouse from 2020-02-10 to 2023-12-30.

STEP 6: After completion of the chart review and ready to check the plot function 6, close the image by clicking on the x button on the top-right side of the image.


PLOT FUNCTION 6: plot_temperature_line_chart(city_name, city_weather_records, date_from, date_to)

STEP 1: The Visual Studio code clicked run code button from plot function 1 will start the execution of this plot function 6 automatically after the chart image of the plot function 5 is closed.

STEP 2: Enter the City ID (or press 'c' to cancel): 
	Choose from the available Available Cities in the format: [City ID = City Name] [1 = Middlesbrough; 2 = London; 3 = Paris; 4 = Toulouse; 5 = Lagos; 6 = Leeds]
	Example: Enter the City ID (or press 'c' to cancel): 6
	Note that the plot function will be terminated and the phase 2 program will come to an end, if you press c as an input through-out this plot function 6 program. 
	You can restart the program, if necessary, by clicking on the run code button if the program ends, hence, restarting the program from plot function 1.

STEP 3: Please, specify the start date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the start date in YYYY-MM-DD format: 2020-01-15

STEP 4: Please, specify the end date in YYYY-MM-DD format: 
	Choose from the available date range in the submitted database: 2020-01-01 - 2024-12-27
	Example: Please, specify the end date in YYYY-MM-DD format: 2024-12-20
	
STEP 5: Output Example: Line chart plot showing the line chart for the minimum temperature, maximum temperature and the mean temperature for Leeds from 2020-01-15 to 2024-12-20.

STEP 6: After completion of the chart review and ready to exit the program to check phase 3 or to restart phase 2, close the image by clicking on the x button on the top-right side of the image.


PHASE 3 - FUNCTIONS FOR RETRIEVING WEATHER API DATE TO THE DATABASE

DEPENDENCY INFORMATION: The dependencies required to run the phase 3 program are os module, sqlite3 module, datetime module, requests module, geopy module and the timezonefinder module.

pip install requests, pip install geopy and pip install timezonefinder should be used to install requests module, geopy module and timezonefinder module respectively from the CMD prompt on windows. 
You can research how to install requests module, geopy module and timezonefinder module in Python if you are using another operating system.

The os module, sqlite3 module and datetime module are Python in-built modules.

Internet connection is required to run this phase 3 program.

The phase 3 of the ICA is a program written to retrieve weather data from open-meteo API and save the retrieved data into the SQLite database.

The cities and the parameters to be downloaded are hardcoded into the program while geopy and timezonefinder were incorporated into the program to generate the latitude, longitude, country name and the timezone automatically by using the hardcoded cities in the program.

The inputs required to run the program are the start date and the end date. Note that the program is designed to only function if the input end date is less than 2 days from the date the program is run.

The following are the steps to use the program to download the weather API data.

STEP 1: Click on the Visual Studio code run code button of the python script

STEP 2: Enter the start date (YYYY-MM-DD):
	Example: Enter the start date (YYYY-MM-DD): 2020-02-02

STEP 3: Enter the end date (YYYY-MM-DD): 
	Example: Enter the end date (YYYY-MM-DD): 2020-02-05

STEP 4: Output: Dates are valid!
		Database initialized successfully!
		Weather data for Lagos saved successfully!
		Weather data for Middlesbrough saved successfully!
		Weather data for London saved successfully!
		Weather data for Leeds saved successfully!
		Weather data for Paris saved successfully!
		Weather data for Toulouse saved successfully!

STEP 5: You can re-click on the Visual Studio run code button if there is need to download for another range of dates or close the program Visual Studio python script to exit the program.


PHASE 4 - WEATHER DOWNLOAD APPLICATION USING GRAPHICAL USER INTERFACE (GUI)

PHASE 4 (1) - WEATHER DOWNLOAD APPLICATION USING GRAPHICAL USER INTERFACE (GUI) FROM THE PHASE 4 PYTHON SCRIPT

DEPENDENCY INFORMATION: The dependencies required to run the phase 4 program are os module, sys module, sqlite3 module, tkinter module and the phase 3 module of this ICA.

pip install requests, pip install geopy and pip install timezonefinder should be used to install requests module, geopy module and timezonefinder module respectively from the CMD prompt on windows. 
You can research how to install requests module, geopy module and timezonefinder module in Python if you are using another operating system.

The os module, sys module, sqlite3 module and tkinter module are Python in-built modules. 

Ensure the phase 3 Python script (module) is in the same folder directory you are executing this phase 4 Python script from.

Internet connection is required to run both of these phase 4 programs.

The inputs required to run the program are the start date and the end date. Note that the program is designed to only function if the input end date is less than 2 days from the date the program is run.

The following are the steps to use the program to download the weather API data.

STEP 1: Click on the Visual Studio code run code button of the python script

STEP 2: Enter the start date (YYYY-MM-DD) in the Graphical Interface that will prompt out after the run code button is clicked:
	Example: Start Date (YYYY-MM-DD): 2022-03-08

STEP 3: Enter the end date (YYYY-MM-DD) in the Graphical Interface that will prompt out after the run code button is clicked: 
	Example: End Date (YYYY-MM-DD): 2022-04-10

STEP 4: Output: A separate notification window displaying "Weather data fetched and stored successfully"
	Note that the data has been successfully downloaded into the SQLite database after the message is displayed.


PHASE (2) - WEATHER DOWNLOAD APPLICATION USING GRAPHICAL USER INTERFACE (GUI) AS A STANDALONE GUI APPLICATION

The standalone GUI application was created with pyinstaller.

The pyinstaller was installed with pip install pyinstaller from the CMD prompt on windows.

The standalone GUI application was created by changing the directory on the CMD to the folder containing the phase 4 python script. Then, pyinstaller --onefile --windowed phase 4.py was run on the CMD prompt on windows.

DEPENDENCY INFORMATION: The dependencies required to run the standalone GUI application is to ensure it is run from the folder containing the SQLite database folder, such as the directory to the database location is db/SQLite database.

Internet connection is required to run both of these phase 4 programs.

The inputs required to run the program are the start date and the end date. Note that the program is designed to only function if the input end date is less than 2 days from the date the program is run.

The following are the steps to use the program to download the weather API data.

STEP 1: Click on the standalone GUI application

STEP 2: Enter the start date (YYYY-MM-DD) in the Graphical Interface that will prompt out after the run code button is clicked:
	Example: Start Date (YYYY-MM-DD): 2022-03-08

STEP 3: Enter the end date (YYYY-MM-DD) in the Graphical Interface that will prompt out after the run code button is clicked: 
	Example: End Date (YYYY-MM-DD): 2022-04-10

STEP 4: Output: A separate notification window displaying "Weather data fetched and stored successfully".
	Note that the data has been successfully downloaded into the SQLite database after the message is displayed.



HOW TO RUN THE TEST FOR PHASE 1 TO PHASE 4
Please, refer to the attached blackbox test entries. You can use the attached blackbox entries as guide. You should simply enter an invalid parameter into the inputs while ensuring the connection to the database is okay, and ensure there is active internet connection to run both of the phase 4 programs..











