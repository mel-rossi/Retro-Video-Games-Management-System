import numpy as np
import pandas as pd
from flask_cors import CORS
from RentalStat import rent_num
from RentalStat import active_filter 
from RentalStat import inactive_filter
from RentalStat import avg_rental_time
from fetchDetails import get_r, get_g
from flask import request, jsonify, Blueprint 
from validateEntries import validateVideoGameID

# This program Outputs Rental History based off of Video Game (ID or Title) 

# Blueprint
gamerental_bp = Blueprint('GameRental', __name__)
CORS(gamerental_bp)

# Global Variables 
df_r = get_r() # Rentals DataFrame
df_g = get_g() # (Video) Games DataFrame

# Filter Rentals by Video Game 
def game_filter(VideoGameInput): 

    return df_r[df_r['VideoGameID'] == VideoGameInput].copy()
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

# Number of unique Video Game IDs rented out 
def game_num(df):

    rentals = active_filter(df)
    return len(rentals)
# game_num

# Process Input
def find_game(userInput=None, output=None):

    empty = pd.DataFrame()

    if userInput is None: 
        return empty, empty, empty, empty

    # Video Game ID input if only 4 digits
    if userInput.isdigit() and len(userInput) == 4: 
        userInput = "V" + userInput

    # Video Game ID input with V + 4 digits
    elif userInput.startswith("V") and len(userInput) == 5: 
        pass

    # Video Game Title input 
    else:
        # Retrieve VideoGameID associated with Title
        userInput = df_g.loc[df_g['Title'].str.lower() == userInput.lower(), \
                             'VideoGameID'].values
        
        # Invalid Title input
        if len(userInput) <= 0: 
            return empty, empty, empty, empty
        elif len(userInput) == 1: 
            userInput = userInput[0]
             
    # Video Game ID input validation
    if validateVideoGameID(userInput):
        # Retrieve Video Game details based on VideoGameID
        game = df_g[df_g['VideoGameID'] == userInput] 

        # Check whether rentals of this VideoGameID exist 
        exist = rental_exist(userInput)

        # Filter Rentals by Video Game 
        rentals = game_filter(userInput) 

        # There is at least one Rental with VideoGameID
        if exist:
            
            # Only Video Game Stat is desired 
            if not output == None and output.lower() == 'stat': 
                activeRentals = empty 
                inactiveRentals = empty
            else: 
                # Rentals (active & inactive) rentals with this VideoGameID 
                activeRentals, inactiveRentals = rental_info(rentals) 

            # Calculate average Rental Time of said Video Game 
            average = avg_rental_time(rentals)
            average = pd.DataFrame([average], columns=['Rental Time Average'])

            # Calculate how many times said Video Game has been Rented Out 
            numRent = rent_num(rentals) 
            numRent = pd.DataFrame([numRent], columns=['Numbers of Rentals'])

            # Calculate how many copies of said Video Game has been Rented out 
            rentedNum = game_num(rentals)
            rentedNum = pd.DataFrame([rentedNum], \
                        columns=['Number of Copies Rented Out']) 

            # Merge average & numRentals into one row
            rentalStats = pd.concat([average, numRent, rentedNum], axis=1)

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
    
    global df_r, df_g
    df_r = get_r() # Rentals DataFrame
    df_g = get_g() # (Video) Games DataFrame

    data = request.json # Get json data from POST body 
    game, activeRentals, inactiveRentals, rentalStats = \
            find_game(data.get('option'), data.get('out'))
   
    if activeRentals.empty and inactiveRentals.empty: 
        data = { 
            "Video Game": game.to_dict(orient='records'), 
            "Rental Stats": rentalStats.to_dict(orient='records')
        } 
    else: 
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
