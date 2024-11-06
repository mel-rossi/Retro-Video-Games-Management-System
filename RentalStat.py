import os 
import pandas as pd 
from flask_cors import CORS
from validateEntries import generateDate
from flask import request, jsonify, Blueprint

# This program Outputs Rental Statistics and Rental History :
# Retrieves Rentals : unbiased, active or inactive 
# Calculates Rental Stats : Number of Rentals & Average Rental Time 

rentalstat_bp = Blueprint('RentalStat', __name__) 
CORS(rentalstat_bp) 

# Load the .csv file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv') 

# Read .csv file into DataFrame 
df = pd.read_csv(RENTAL_PATH)

# Filter Rentals by Rental ID 
def rental_filter(RentalInput): 
    
    return df[df['RentalID'] == RentalInput].copy() 
# rental_filter

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
    rentals = rentals.drop(columns=['Status']) 

    return rentals
# inactive_filter 

# Calculate : Average Rental Time ([Return - Start Date] mean) 
def avg_rental_time(rentals): 

    today = pd.to_datetime(generateDate())

    # Convert date columns to datetime 
    rentals['StartDate'] = pd.to_datetime(rentals['StartDate'], errors='coerce')
    startDate = rentals['StartDate']

    # Replace empty ReturnDate with today's date
    if 'ReturnDate' not in rentals.columns or (rentals['ReturnDate'] == '-1').any(): 
        returnDate = today
        
    else:
        rentals['ReturnDate'] = pd.to_datetime(rentals['ReturnDate']) 
        returnDate = rentals['ReturnDate']

    # Calculate rental duration in days 
    rentals['RentalDuration'] = (returnDate - startDate).dt.days 
    average = rentals['RentalDuration'].mean()

    return average 
# avg_rental_time 

# Calculate : How many times it has been rented out 
def rent_num(rentals): 

    # Number of rentals 
    num = len(rentals)

    return num 
# rent_num

# How many times a game was rented by month
def game_rent_by_month(VideoGameID, rangeM=None, rangeY=None):
    from GameRental import game_filter

    rentals = game_filter(VideoGameID) # Filter rentals by Video Game

    if rentals.empty: 
        count = pd.Series(0, index=range(1, 13))
    else: 
        # Convert StartDate to date time 
        rentals['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')

        # Extract Year and Month from StartDate 
        rentals['Year'] = rentals['StartDate'].dt.year
        rentals['Month'] = rentals['StartDate'].dt.month

        # If range is provided 
        if rangeM or rangeY:
            # Parse range 
            if rangeM: 
                start_month, end_month = map(int, rangeM.split('-')) # parse month range 
                filters = ((rentals['Month'] >= start_month) & (rentals['Month'] <= end_month))

            if rangeY: 
                start_year, end_year = map(int, rangeY.split('-')) # Parse year range 
                filters = ((rentals['Year'] >= start_year) & (rentals['Month'] <= end_year)) 

            if rangeY and rangeM:
                filters = ((rentals['Year'] == start_year) & (rentals['Month'] >= start_month)) 
                filters |= ((rentals['Year'] == end_year) & (rentals['Month'] <= end_month))
                filters |= ((rentals['Year'] > start_year) & (rentals['Year'] < end_year)) 

            # Filter rentals by the range 
            rentals = rentals[filters]

        # Count by month
        count = rentals['Month'].value_counts().sort_index() 

    # Dictionary with month names 
    months = { 
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec' 
    }

    # Ensure all months are included, even if count is 0
    allMonths = pd.Series(0, index=months.keys()).rename(index=months)
    count = allMonths.add(count.rename(index=months), fill_value=0).astype(int) 

    # Convert to DataFrame then to dictionary
    countDict = { 
        "Rentals by Month": [{month: int(count[month])} for month in months.values()]
    }

    return countDict
    #return countDict # for Testing purposes
    #return jsonify(countDict)
# game_rent_by_month 

# Organize Rental Information
def rental_info(status):

    # Default : Unbiased Rental Stats
    rentals = df

    if status is not None: 
        # 'Inactive' Rental Stats
        if status.lower() == 'active':
            rentals = active_filter(rentals) 

        # 'Inactive' Rental Stats
        elif status.lower() == 'inactive': 
            rentals = inactive_filter(rentals)

    # Calculate average Rental Time
    average = avg_rental_time(rentals)
    average = pd.DataFrame([average], columns=['Rental Time Average']) # Convert to DataFrame 

    # Calculate how many rentals there have been 
    num = rent_num(rentals)
    num = pd.DataFrame([num], columns=['Numbers of Rentals']) # Convert to DataFrame

    # Testing game_rent_by_month 
    # Calculate how many rentals there have been per month
    #IDs = { 'id': ['V0055', 'V0188', 'V0002', 'V0797', 'V0770', 'V1790', 'V0790', 'V0109', 'V0072', 'V1008', 
    #              'V0089', 'V0111', 'V0011', 'V0080', 'V0190', 'V0998', 'V0820', 'V0189', 'V0371', 'V1792', 
    #              'V0486', 'V0281', 'V0036', 'V0021', 'V0030', 'V0668', 'V0090', 'V0283', 'V0902', 'V0001'] }
    #for GameID in IDs['id']: 
    #    numMonth = game_rent_by_month(GameID, '8-9', None) 
    #    print(f'{GameID} : {numMonth}') 

    # Drop 'RentalDuration' column 
    rentals = rentals.drop(columns=['RentalDuration'])
    
    # Merge average & numRentals into one row
    rentalStats = pd.concat([average, num], axis=1)

    # Ensure date columns are formatted consistently
    rentals['StartDate'] = rentals['StartDate'].dt.strftime('%Y-%m-%d')

    return rentals, rentalStats
# rental_info

@rentalstat_bp.route('/rental_stat', methods=['POST']) 
def rental_stat_route():

    data = request.json # Get json data from POST body 

    option = data.get('option').lower()

    if option is not None: # Check if option is provided
        if option == 'history': # Get rental history
            game_id = data.get('id')
            month_range = data.get('month_range')
            year_range = data.get('year_range')
            data = game_rent_by_month(game_id, month_range, year_range)

        elif option == 'rental': # Get rental info
            user_input = data.get('status') # Extract 'status' field
            rentals, rentalStats = rental_info(user_input)
            data = { 
                "Rentals": rentals.to_dict(orient='records'), 
                "Rental Stats": rentalStats.to_dict(orient='records') 
            }       
        else:
            return jsonify({ "error": "Invalid option provided" }), 400
    else:
        return jsonify({ "error": "No option provided" }), 400


    return jsonify(data)
# rental_stat_route