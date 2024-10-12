# This program Shows History based off of the Video Game

# Imports 
from flask import Flask, jsonify, request
import pandas as pd 
from validateEntries import generateDate
from flask_cors import CORS
import numpy as np


app = Flask(__name__)
CORS(app)

# Data Frames 

# Load Rentals & Video Games
df1 = pd.read_csv('Inventory/Rentals.csv')
df2 = pd.read_csv('Inventory/VideoGames.csv')

# Functions

# Filter Rental rows where VideoGameID matches VideoGameInput 
def filter_rentals(VideoGameInput): 
    return df1[df1['VideoGameID'] == VideoGameInput].copy()
# filter_rentals

# Check whether Rentals of said videoGame exist
def rental_exist(VideoGameInput): 
    return not filter_rentals(VideoGameInput).empty
# rental_exist 

# Organize Rental Information of VideoGameID
def rental_info(VideoGameInput): 
    # Filter relevant rentals 
    rentals = filter_rentals(VideoGameInput) 

    # Display Rental Registrations based on VideoGameID
    info = "" 
    for index, row in rentals.iterrows(): 
        dic = row.to_dict() # Convert to dictionary 
        for key, value in dic.items(): 
            info += f"{key}: {value}\n"
        info += '\n' # Add a newline between entries

    return info 
# rental_info 

# Calculate : Average Rental Time (Return - Start Date)
def avg_rental_time(VideoGameInput):
    # Filter relevant rentals 
    rentals = filter_rentals(VideoGameInput) 

    # Convert date columns to datetime
    rentals['StartDate'] = pd.to_datetime(rentals['StartDate'])
    rentals['ReturnDate'] = pd.to_datetime(rentals['ReturnDate'])

    # Replace empty ReturnDate with today's data
    today = pd.to_datetime(generateDate())
    rentals['ReturnDate'] = rentals['ReturnDate'].fillna(today)

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

    # Iterate through teh column VideoGameID in Rentals 
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

    # Convert sorted Games DataFrame to dictionary 
    sortedGames = sortedGames.to_dict(orient='records')

    # Return sorted Games
    return sortedGames
# rank

def route_input(userInput):
    # Rank Rentals based on numRentals 
    if userInput.lower() == 'rank':
        sortedRentals = rank() 
        # print(sortedRentals)
        return sortedRentals

    # Number of active Rentals
    elif userInput.lower() == 'active': 
        active = active_rentals()
        return active

    # Number of inactive Rentals 
    elif userInput.lower() == 'inactive': 
        inactive = inactive_rentals()
        return inactive
    
    # Number of all Rentals ever made
    elif userInput.lower() == 'all': 
        rentalsEver = all_rentals()
        return rentalsEver

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
            return None
        elif len(userInput) == 1: 
            userInput = userInput[0]
             
    # Video Game ID input validation
    if userInput.startswith("V") and len(userInput) == 5: 
        # Check if VideoGameID is valid
        if userInput >= "V0000" and userInput <= "V6000" and userInput[1:].isdigit(): # V0000 - V6000
            # Check whether rentals of this VideoGameID exist 
            exist = rental_exist(userInput)

            # There is at least one Rental with VideoGameID
            if exist: 
                # Rentals related to inputed VideoGameID 
                rentalData = rental_info(userInput)

                # Calculate average Rental Time of said Video Game 
                average = avg_rental_time(userInput)

                # Calcultae how many times said Video Game has been Rented Out 
                numRentals = rent_num(userInput) 

                return f"Rentals: {rentalData} Rental Time Average: {average} Number of Rentals: {numRentals}"

            # No Rentals with VideoGameID 
            else:
                return "Rentals: 0"

        # Invalid VideoGameID 
        else: 
            return None

# get_input

@app.route('/game_rental', methods=['GET', 'POST']) # Both GET and POST are possible 
def game_rental_route():
    if request.method == 'POST': 
        VideoGameID = request.json.get('input')
    else: 
        VideoGameID = request.args.get('input')

    videoGame = route_input(VideoGameID)

    if videoGame: 
        return jsonify(videoGame)
    else: 
        return jsonify({"error": "No special call nor video game with provided ID or name"}), 404

if __name__ == '__main__':
    app.run(debug=True)
