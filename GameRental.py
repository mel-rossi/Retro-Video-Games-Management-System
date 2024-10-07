# This program Shows Hisory based off of the Video Game instead of the Member

# BIG WIP

# Imports 
import pandas as pd 
from validateEntries import generateDate

# Data Frames 

# Read Rentals
df1 = pd.read_csv('Inventory/Rentals.csv')

# Read VideoGames 
df2 = pd.read_csv('Inventory/VideoGames.csv')
                          

# Functions

# Filter rows where VideoGameID matches VideoGameInput 
def filterRentals(VideoGameInput): 
    return df1[df1['VideoGameID'] == VideoGameInput].copy()
# filterRentals

# Print out Rental Information of VideoGameID
def RentalInfo(VideoGameInput): 
    print("This are the Rental registrations of the following Video Game: ")
    
    # Filter relevant rentals 
    rentals = filterRentals(VideoGameInput) 

    # Display Rental Registrations based on VideoGameID

    if rentals.empty:
        print("No Rentals for this Video Game were made.")
        return False # VideoGameID doesn't appear in Rentals at all
    else: 
        for index, row in rentals.iterrows(): 
            dic = row.to_dict() # Convert to dictionary 
            for key, value in dic.items(): 
                print(f"{key}: {value}")
        return True # VideoGameID appears in Rentals at least once 
# RentalInfo 

# Calculate average Rental Time (Return - Start Date)
def avgRentalTime(VideoGameInput, exist):
    # No Rentals with Video Game ID 
    if not exist: 
        return None 

    # Filter relevant rentals 
    rentals = filterRentals(VideoGameInput) 

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

    print(f"The average Rental Time of the following Video Game is {average} days.")
# avgRentalTime 

# How many times VideoGame ID has been rented out 

# Rank based on number of times VideoGames have been rented out 

# How many VideoGame IDs are currently active rentals

# How many rentals have there been ever 

while True: 
    # Note: Add Title input later 
    VideoGameID = input("Enter Video Game ID (V####), or type exit to quit: ").strip()

    if VideoGameID.lower() == 'exit': 
        print("Exiting the program.") 
        break 

    # Note: Add validation for existent Video Game ID here. 
   
    rentalExist = RentalInfo(VideoGameID) 
    
    avgRentalTime(VideoGameID, rentalExist)


