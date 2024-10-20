# This program calculate Rental Stats 

import os 
import pandas as pd 
from flask_cors import CORS
from validateEntries import generateDate
from flask import request, jsonify, Blueprint 

rentalstat_bp = Blueprint('RentalStat', __name__) 
CORS(rentalstat_bp) 

# Load the .csv file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv') 

# Read .csv file into DataFrame 
df = pd.read_csv(RENTAL_PATH)

# Functions 

# Filter rentals by active rentals 
def active_filter(rentals):
    
    rentals = rentals[rentals['Status'] == 'Active'].copy() 

    # Drop the 'Status' and 'ReturnDate' columns 
    rentals = rentals.drop(columns=['Status', 'ReturnDate'])
    
    return rentals
# active_filter 

# Filter rentals by inactive rentals 
def inactive_filter(rentals): 

    rentals = rentals[rentals['Status'] == 'Inactive'].copy() 

    # Drop the 'Status' column 
    #rentals = rentals.drop(columns=['Status']) 

    return rentals
# inactive_filter 

# Calculate : Average Rental Time ([Return - Start Date] mean) 
def avg_rental_time(rentals): 

    today = generateDate()

    # Convert date columns to datetime 
    rentals['StartDate'] = pd.to_datetime(rentals['StartDate'])
    startDate = rentals['StartDate']

    # Replace empty ReturnDate with today's date
    if 'ReturnDate' not in df.columns or (df['ReturnDate'] == '-1').any(): 
        returnDate = pd.to_datetime(today)
        
    else:
        rentals['ReturnDate'] = pd.to_datetime(rentals['ReturnDate']) 
        returnDate = rentals['ReturnDate'] 

    # Calculate rental duration in days 
    rentals['RentalDuration'] = (returnDate - startDate).dt.days 

    average = rentals['RentalDuration'].mean()

    average = pd.DataFrame([average], columns=['Rental Time Average'])

    return average 
# avg_rental_time 

# Calculate : How many times it has been rented out 
def rent_num(Input, idName): 

    # Initialize number of rentals 
    num = 0

    # Iterate through the column 

    # Unbiased 
    if idName is None: 
        num = len(df)

    # Biased by ID of idName
    else:
        for ID in df[idName]: 
            if ID == Input: 
                num += 1

    num = pd.DataFrame([num], columns=['Numbers of Rentals']) 

    return num 
# rent_num

def route_input(status):

    rentals = df
    idName = None 
    idInput = None

    if status is not None:
        # If filtered by 'Active' Rentals 
        if status.lower() == 'active': 
            idName = 'Status'
            idInput = 'Active'
        # If filtered by 'Inactive' Rentals 
        elif status.lower() == 'inactive': 
            rentals = inactive_filter(rentals)
            idName = 'Status' 
            idInput = 'Inactive'

    # Calculate average Rental Time
    average = avg_rental_time(rentals)

    # Calculate how many rentals there have been 
    numRentals = rent_num(idInput, idName)

    # Drop 'RentalDuration' column 
    rentals = rentals.drop(columns=['RentalDuration'])
    
    # Merge average & numRentals into one row
    rentalStats = pd.concat([average, numRentals], axis=1)

    return rentals, rentalStats
# route_input

@rentalstat_bp.route('/rental_stat', methods=['POST']) 
def rental_stat_route():

    data = request.json # Get json data from POST body 
    user_input = data.get('status') # Extract 'status' field

    rentals, rentalStats = route_input(user_input) 

    data = { 
        "Rentals": rentals.to_dict(orient='records'), 
        "Rental Stats": rentalStats.to_dict(orient='records') 
    } 

    return jsonify(data)
# rental_stat_route




