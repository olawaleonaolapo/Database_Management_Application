# Author: <Olawale Francis Onaolapo>
# 

##############################################################################
# IMPORTED LIBRARIES - FOR API WEATHER DATA DOWNLOAD USING TkinKer GUI
##############################################################################
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sqlite3
import sys
from phase_3 import (
    initialize_db,
    db_connection,
    get_city_details,
    validate_dates,
    retrieve_and_store_weather_data,
)

############################################
# DEFAULT CITIES
############################################
DEFAULT_CITIES = ["Lagos", "Middlesbrough", "London", "Leeds", "Paris", "Toulouse"]


##############################################
# FUNCTION TO SET UP THE WORKING DIRECTORY
##############################################
def change_to_executable_directory():
    """
    To change to the script or executable location from the current working directory.
    """
    if getattr(sys, 'frozen', False):  # To check if running as a PyInstaller executable
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(__file__))


def get_database_path():
    """
    Constructs the full path to the database file in the 'db' directory under the executable/script folder.
    """
    base_dir = os.getcwd()
    db_dir = os.path.join(base_dir, "db")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return os.path.join(db_dir, "CIS4044-N-SDI-OPENMETEO-PARTIAL.db")


##############################################
# FUNCTION TO INITIALIZE THE DATABASE
##############################################
def setup_database():
    """
    Initializes the database structure if not already set up.
    """
    try:
        db_path = get_database_path()
        connection = db_connection(db_path)
        initialize_db(connection)
        messagebox.showinfo("Success", "Database initialized successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error initializing the database: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")


#################################################
# FUNCTION TO UPDATE THE DATABASE FROM THE GUI
#################################################
def update_sdi_ica_database(start_date, end_date):
    """
    Updates the database using start date and end date inputs from the GUI.
    """
    try:
        validate_dates(start_date, end_date)
    except ValueError as e:
        messagebox.showerror("Date Validation Error", str(e))
        return

    try:
        db_path = get_database_path()
        connection = db_connection(db_path)
        initialize_db(connection)
    except Exception as e:
        messagebox.showerror("Database Error", f"Error initializing the database: {e}")
        return

    try:
        for city_name in DEFAULT_CITIES:
            try:
                city_details = get_city_details(city_name)
                retrieve_and_store_weather_data(city_name, city_details, db_path, start_date, end_date)
            except ValueError as e:
                print(f"Error fetching data for {city_name}: {e}")
                continue
        messagebox.showinfo("Success", "Weather data fetched and stored successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


############################################################
# FUNCTION TO HANDLE UPDATE SDI-ICA DB BUTTON CLICK EVENT
############################################################
def weather_retrieval_request(start_date_entry, end_date_entry):
    """
    Handles the click event for the Update button.
    """
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()
    update_sdi_ica_database(start_date, end_date)


##############################################
# FUNCTION TO CREATE THE Tkinter UI
##############################################
def create_sid_ica_ui():
    """
    Creates the Tkinter window, input fields, and buttons.
    """
    sdi_root = tk.Tk()
    sdi_root.title("SDI-ICA Weather Database Updater")

    sdi_frame = ttk.Frame(sdi_root, padding="70")
    sdi_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(sdi_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, pady=5)
    start_date_entry = ttk.Entry(sdi_frame, width=20)
    start_date_entry.grid(row=0, column=1, pady=5)

    ttk.Label(sdi_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
    end_date_entry = ttk.Entry(sdi_frame, width=20)
    end_date_entry.grid(row=1, column=1, pady=5)

    def update_sdi_ica_db_button():
        weather_retrieval_request(start_date_entry, end_date_entry)

    update_button = ttk.Button(
        sdi_frame,
        text="Update SDI-ICA Database",
        command=update_sdi_ica_db_button
    )
    update_button.grid(row=2, column=1, pady=15)

    start_date_entry.focus()
    sdi_root.mainloop()


#####################################################
# MAIN EXECUTION SECTION
#####################################################
def main():
    """
    Main entry point to run the program.
    """
    change_to_executable_directory()
    create_sid_ica_ui()


if __name__ == "__main__":
    main()
