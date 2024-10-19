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
def active_filter(df=df):
    
    df[df['Status'] == 'Active'].copy() 

    # Drop the 'Status' and 'ReturnDate' columns 
    df = df.drop(columns=['Status', 'ReturnDate'])
    
    return df
# active_filter 

# Filter rentals by inactive rentals 
def inactive_filter(df=df): 

    df[df['Status']== 'Inactive'].copy 

    # Drop the 'Status column 
    df = df.drop(columns=['Status']) 

    return df
# inactive_filter 

# Organize Rental Information : remove later  
def rental_info(df=df): 
    
    return df
# rental_info 

def avg_rental_time(df): 
    
    # Replace empty (-1) ReturnDate with today's date 
    today = generateDate() 
    df['ReturnDate'] = df['ReturnDate'].replace('-1', today) 

    # Convert date columns to datetime 
    df['StartDate'] = pd.to_datetime(df['StartDate']) 
    df['ReturnDate'] = pd.to_datetime(df['ReturnDate']) 

    # Calculate rental duration in days 
    df['RentalDuration'] = (df['ReturnDate'] - df['StartDate']).dt.days 

    average = df['RentalDuration'].mean()

    average = pd.DataFrame([average], columns=['Rental Time Average']) 

    return average 
# avg_rental_time 

# Calculate : How many times it has been rented out 
def rent_num(Input, idName): 

    # Initialize number of rentals 
    num = 0

    # Iterate through the column 
    for ID in df[idName]: 
        if ID == Input: 
            num += 1

    num = pd.DataFrame([num], columns=['Numbers of Rentals']) 

    return num 
# rent_num 


