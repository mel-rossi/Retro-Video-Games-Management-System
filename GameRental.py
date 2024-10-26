import os
import numpy as np
import pandas as pd
from flask_cors import CORS
from RentalStat import rent_num
from RentalStat import active_filter 
from RentalStat import inactive_filter
from RentalStat import avg_rental_time
from flask import request, jsonify, Blueprint 
from validateEntries import validateVideoGameID

# This program Outputs Rental History based off of Video Game (ID or Title) 

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

# Filter Rentals by Video Game 
def game_filter(VideoGameInput): 

    return df1[df1['VideoGameID'] == VideoGameInput].copy()
# game_filter

# Check whether Rentals of said Video Game exist
def rental_exist(VideoGameInput):

    return not game_filter(VideoGameInput).empty
# rental_exist 

# Organize Rental Information of Video Game
def rental_info(rentals):

    # Drop the 'VideoGameID' column 
    rentals = rentals.drop(columns=['VideoGameID'])

    # Separate rentals into active and inactive rentals 
    activeRentals = active_filter(rentals) 
    inactiveRentals = inactive_filter(rentals) 

    return activeRentals, inactiveRentals 
# rental_info 

# Process Input
def find_game(userInput):

    empty = pd.DataFrame()

    # Video Game ID input if only 4 digits
    if userInput.isdigit() and len(userInput) == 4: 
        userInput = "V" + userInput

    # Video Game ID input with V + 4 digits
    elif userInput.startswith("V") and len(userInput) == 5: 
        pass

    # Video Game Title input 
    else:
        # Retrieve VideoGameID associated with Title
        userInput = df2.loc[df2['Title'].str.lower() == userInput.lower(), 'VideoGameID'].values
        
        # Invalid Title input
        if len(userInput) <= 0: 
            return empty, empty, empty, empty
        elif len(userInput) == 1: 
            userInput = userInput[0]
             
    # Video Game ID input validation
    if validateVideoGameID(userInput):
        # Retrieve Video Game details based on VideoGameID
        game = df2[df2['VideoGameID'] == userInput] 

        # Check whether rentals of this VideoGameID exist 
        exist = rental_exist(userInput)

        # Filter Rentals by Video Game 
        rentals = game_filter(userInput) 

        # There is at least one Rental with VideoGameID
        if exist: 
            # Rentals (active & inactive) rentals with this VideoGameID  
            activeRentals, inactiveRentals = rental_info(rentals)

            # Calculate average Rental Time of said Video Game 
            average = avg_rental_time(rentals)

            # Calcultae how many times said Video Game has been Rented Out 
            numRentals = rent_num(rentals) 

            # Merge average & numRentals into one row
            rentalStats = pd.concat([average, numRentals], axis=1)

            return game, activeRentals, inactiveRentals, rentalStats

        # No Rentals with VideoGameID 
        else:
            return game, empty, empty, empty

    # Invalid VideoGameID 
    else: 
        return empty, empty, empty, empty
# find_game

@gamerental_bp.route('/game_rental', methods=['POST']) 
def game_rental_route():
    
    data = request.json # Get json data from POST body 
    user_input = data.get('option') # Extract 'option' field 

    game, activeRentals, inactiveRentals, rentalStats = find_game(user_input)

    data = {
        "Video Game": game.to_dict(orient='records'), 
        "Active Rentals": activeRentals.to_dict(orient='records'), 
        "Inactive Rentals": inactiveRentals.to_dict(orient='records'), 
        "Rental Stats": rentalStats.to_dict(orient='records'), 
     } 

    # Valid Input 
    if not game.empty: 
        return jsonify(data)

    # Invalid Input
    else: 
        return jsonify({"error": "No video game found with the provided ID or title."}), 404
