# This program Shows Hisory based off of the Video Game instead of the Member

# BIG WIP

# Imports 
import pandas as pd 

# Data Frames 

# Read Rentals
df1 = pd.read_csv('Inventory/Rentals.csv')

# Read VideoGames 
df2 = pd.read_csv('Inventory/VideoGames.csv')
                          

# Functions 

# Print out Rental Information of VideoGameID
def RentalInfo(VideoGameInput): 
    print("This are the Rental registrations of the the following Game ID: ")
    
    # Filter rows where VideoGameID matches VideoGameInput 
    rentals = df1[df1['VideoGameID'] == VideoGameInput] 

    # Display Rental Registrations based on VideoGameID

    if rentals.empty: # VideoGameID doesn't appear in Rentals at all
        print("No Rentals for this Video Game were made.")
    else: 
        for index, row in rentals.iterrows(): 
            dic = row.to_dict() # Convert to dictionary 
            for key, value in dic.items(): 
                print(f"{key}: {value}")
# RentalInfo 

# Calculate average Rental Time (Start - Return Date) 

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
    
    RentalInfo(VideoGameID)


