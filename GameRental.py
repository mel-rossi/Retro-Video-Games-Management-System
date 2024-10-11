# This program Shows History based off of the Video Game

# Flask WIP

# Imports 
from flask import Flask, jsonify, request
import pandas as pd 
from validateEntries import generateDate

app = Flask(__name__)

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

    # No Rentals with Video Game ID
    if rentals.empty: 
        return None 

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
def avg_rental_time(VideoGameInput, exist):
    # No Rentals with Video Game ID 
    if not exist: 
        return None 

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
def rent_num(VideoGameInput, exist):
    # No Rentals with Video Game ID
    if not exist:
        return None

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
        numRentals = rent_num(VideoGameID, exist) 
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
    # Rank Rentals based on numRentals 
    if userInput.lower() == 'rank':
        sortedRentals = rank() 
        print(sortedRentals)

    # Number of active Rentals
    elif userInput.lower() == 'active': 
        active = active_rentals()
        print(f"There are currently {active} Active Rentals. \n")

    # Number of inactive Rentals 
    elif userInput.lower() == 'inactive': 
        inactive = inactive_rentals()
        print(f"There are currently {inactive} Inactive Rentals. \n")
    
    elif userInput.lower() == 'all': 
        rentalsEver = all_rentals()
        print(f"There have been {rentalsEver} Rentals in Total thus far. \n")

    #elif 

# get_input

# Run
def main(): # Change name later
    VideoGameID = input("Enter one of these:" +  
                "\n\t'V####' (a Video Game ID) to see the Rental History of the Video Game its associated with," + 
                "\n\t'rank' to see the ranking of Video Games based on how often they have been rented out," + 
                "\n\t'active' to find out how many Video Games are currently being rented out," + 
                "\n\t'inactive' to find out how many fulfilled (closed) Rental Transations there have been," + 
                "\n\t'all' to find out how many total Rental Transations there have been" + 
                "\n\t'exit' to quit: ").strip()

    print('\n')

    videoGame = route_input(VideoGameID)
   
    exist = rental_exist(VideoGameID)  

    # Rentals related to inputed VideoGameID
    rentalData = rental_info(VideoGameID)
    if rentalData != None:
        print(rentalData)
    
    # Calculate average Rental Time of said Video Game 
    average = avg_rental_time(VideoGameID, exist)
    if average != None: 
        print(f"The average Rental Time of the following VideoGame is {average} days.")

    # Calculate how many times said Video Game has been Rented 
    numRentals = rent_num(VideoGameID, exist)
    if numRentals == None: 
        print("No Rentals of this Game have been made.")
    else: 
        print(f"This Video Game has been rented out {numRentals} time(s) before.")
    print('\n')

if __name__ == '__main__': 
    main() # Change later
