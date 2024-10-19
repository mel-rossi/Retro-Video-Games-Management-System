# This program Shows History based off of the Video Game

# Imports 
import os
import numpy as np
import pandas as pd
from flask_cors import CORS
from validateEntries import generateDate
from flask import request, jsonify, Blueprint 
from validateEntries import validateVideoGameID

gamerental_bp = Blueprint('GameRental', __name__)
CORS(gamerental_bp)

# Load the .csv files 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv')
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv')

# Read .csv files into DataFrames 
df1 = pd.read_csv(RENTAL_PATH)
df2 = pd.read_csv(VIDEOGAME_PATH)

# Functions

# Filter Rental rows where VideoGameID matches VideoGameInput 
def filter_rentals(VideoGameInput): 

    return df1[df1['VideoGameID'] == VideoGameInput].copy()
# filter_rentals

# Check whether Rentals of said Video Game exist
def rental_exist(VideoGameInput):

    return not filter_rentals(VideoGameInput).empty
# rental_exist 

# Organize Rental Information of Video Game
def rental_info(VideoGameInput):

    # Filter relevant rentals 
    rentals = filter_rentals(VideoGameInput)

    # Separate rentals into active and inactive rentals 
    activeRentals = rentals[rentals['Status'] == 'Active'].copy() 
    inactiveRentals = rentals[rentals['Status'] == 'Inactive'].copy()

    # Drop the 'Status' column
    activeRentals = activeRentals.drop(columns=['Status', 'ReturnDate']) # Additionally drop 'ReturnDate' column
    inactiveRentals = inactiveRentals.drop(columns=['Status'])

    return activeRentals, inactiveRentals 
# rental_info 

# Calculate : Average Rental Time (Return - Start Date)
def avg_rental_time(VideoGameInput):

    # Filter relevant rentals 
    rentals = filter_rentals(VideoGameInput)

    # Replace empty (-1) ReturnDate with today's date 
    today = generateDate()
    rentals['ReturnDate'] = rentals['ReturnDate'].replace('-1', today)

    # Convert date columns to datetime
    rentals['StartDate'] = pd.to_datetime(rentals['StartDate'])
    rentals['ReturnDate'] = pd.to_datetime(rentals['ReturnDate'])

    # Calculate rental duration in days
    rentals['RentalDuration'] = (rentals['ReturnDate'] - rentals['StartDate']).dt.days

    # Calculate the average rental duration 
    average = rentals['RentalDuration'].mean()

    return average
# avg_rental_time 

# Calculate : How many times VideoGameID has been rented out 
def rent_num(VideoGameInput):

    # Filter relevant rentals 
    rentals = filter_rentals(VideoGameInput) 

    # Initialize number of rentals
    num = 0

    # Iterate through the column VideoGameID in Rentals 
    for VideoGameID in df1['VideoGameID']: 
        if VideoGameID == VideoGameInput: 
            num += 1

    return num
# rent_num

# Calculate : How many active rentals are there right now? 
def active_rentals(): 

    active = 0

    # Iterate through Status column in Rentals 
    for Status in df1['Status']: 
        if Status == 'Active': 
            active += 1

    return active
# active_rentals

# Calculate : How many inactive rentals are there right now? 
def inactive_rentals(): 

    inactive = 0

    # Iterate through Status column in Rentals 
    for Status in df1['Status']:
        if Status == 'Inactive': 
            inactive += 1

    return inactive
# inactive_rentals

# Calculate : How many rentals have there been ever? 
def all_rentals(): 

    rentals = 0

    for _, _ in df1.iterrows(): 
        rentals += 1
  
    return rentals
# all_rentals

# Rank Video Games based on number of times they have been rented out
def rank():

    rentals = [] 

    # Iterate through VideoGameID column in Video Games 
    for VideoGameID in df2['VideoGameID']: 
        exist = rental_exist(VideoGameID)  
        numRentals = rent_num(VideoGameID) 
        rentals.append((VideoGameID, numRentals)) 
    
    # Convert to DataFrame for easy sorting 
    sortByRentals = pd.DataFrame(rentals, columns=['VideoGameID', 'rentNum'])

    # Merge rentals with VideoGames DataFrame 
    merge = pd.merge(df2, sortByRentals, on='VideoGameID', how='left')
    merge['rentNum'] = merge['rentNum'].fillna(0) # Fill in no rentals with 0 

    # Sort merged DataFrame by rentNum in descending order
    sortedGames = merge.sort_values(by='rentNum', ascending=False)

    # Drop the 'rentNum' column 
    sortedGames = sortedGames.drop(columns=['rentNum'])

    # Return sorted Games
    return sortedGames
# rank

def route_input(userInput):

    empty = pd.DataFrame()

    # Rank Rentals based on numRentals 
    if userInput.lower() == 'rank':
        sortedRentals = rank() 
        return sortedRentals, empty, "Ranked"

    # Number of total Rentals
    elif userInput.lower() == 'rentals':
        # Number of active Rentals
        active = active_rentals()
        active = pd.DataFrame([active], columns=['Active Total'])

        # Number of inactive Rentals 
        inactive = inactive_rentals()
        inactive = pd.DataFrame([inactive], columns=['Inactive Total'])

        # Number of all Rentals ever made 
        rentalsEver = all_rentals() 
        rentalsEver = pd.DataFrame([rentalsEver], columns=['Total Rentals'])

        # Merge active, inactive and rentalsEver into one row
        numberRentals = pd.concat([active, inactive, rentalsEver], axis=1)
        return numberRentals, empty, "Number of Rentals"

    # Video Game ID input if only 4 digits
    elif userInput.isdigit() and len(userInput) == 4: 
        userInput = "V" + userInput

    # Video Game ID input with V + 4 digits
    elif userInput.startswith("V") and len(userInput) == 5: 
        pass

    # Video Game Title input 
    else: 
        userInput = df2.loc[df2['Title'].str.lower() == userInput.lower(), 'VideoGameID'].values
        
        # Invalid Title input
        if len(userInput) <= 0: 
            return empty, empty, empty
        elif len(userInput) == 1: 
            userInput = userInput[0]
             
    # Video Game ID input validation
    if validateVideoGameID(userInput): 
        # Check whether rentals of this VideoGameID exist 
        exist = rental_exist(userInput)

        # There is at least one Rental with VideoGameID
        if exist: 
            # Rentals related to inputed VideoGameID 
            activeRentals, inactiveRentals = rental_info(userInput)

            # Calculate average Rental Time of said Video Game 
            average = avg_rental_time(userInput)
            average = pd.DataFrame([average], columns=['Rental Time Average']) 

            # Calcultae how many times said Video Game has been Rented Out 
            numRentals = rent_num(userInput) 
            numRentals = pd.DataFrame([numRentals], columns=['Number Of Rentals'])

            # Merge average & numRentals into one row
            rentalStats = pd.concat([average, numRentals], axis=1)

            return activeRentals, inactiveRentals, rentalStats

        # No Rentals with VideoGameID 
        else:
            return empty, empty, empty

    # Invalid VideoGameID 
    else: 
        return empty, empty, empty

# get_input

@gamerental_bp.route('/game_rental', methods=['GET', 'POST']) # Both GET and POST are possible 
def game_rental_route():
    if request.method == 'POST': 
        VideoGameID = request.json.get('option')
    else: 
        VideoGameID = request.args.get('option')

    activeRentals, inactiveRentals, rentalStats = route_input(VideoGameID)

    if isinstance(rentalStats, str):
        data = {
            f"{rentalStats}": activeRentals.to_dict(orient='records') 
        }
    elif not activeRentals.empty:
        data = { 
            "Active Rentals": activeRentals.to_dict(orient='records'), 
            "Inactive Rentals": inactiveRentals.to_dict(orient='records'), 
            "Rental Stats": rentalStats.to_dict(orient='records'), 
        } 


    if not activeRentals.empty: 
        return jsonify(data)
    else: 
        return jsonify({"error": "No special call nor video game with provided ID or name"}), 404

if __name__ == '__main__':
    app.run(debug=True)
