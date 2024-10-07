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

# Filter Rental rows where VideoGameID matches VideoGameInput 
def filterRentals(VideoGameInput): 
    return df1[df1['VideoGameID'] == VideoGameInput].copy()
# filterRentals

# Print out Rental Information of VideoGameID
def RentalInfo(VideoGameInput): 
    # Filter relevant rentals 
    rentals = filterRentals(VideoGameInput) 

    # Display Rental Registrations based on VideoGameID

    if rentals.empty:
        return False # VideoGameID doesn't appear in Rentals at all
    else: 
        print("These are the Rentals registrations of the following Video Game: \n")
        for index, row in rentals.iterrows(): 
            dic = row.to_dict() # Convert to dictionary 
            for key, value in dic.items(): 
                print(f"{key}: {value}")
            print('\n')
        return True # VideoGameID appears in Rentals at least once 
# RentalInfo 

# Calculate : Average Rental Time (Return - Start Date)
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

# Calculate : How many times VideoGameID has been rented out 
def rentNum(VideoGameInput, exist):
    # No Rentals with Video Game ID
    if not exist:
        return None

    # Filter relevant rentals 
    rentals = filterRentals(VideoGameInput) 

    # Initialize number of rentals
    num = 0

    # Iterate through teh column VideoGameID in Rentals 
    for VideoGameID in df1['VideoGameID']: 
        if VideoGameID == VideoGameInput: 
            num += 1

    return num
# rentNum

# Rank Video Games based on number of times they have been rented out
def rank():
    rentals = [] 
    for VideoGameID in df2['VideoGameID']: 
        exist = not filterRentals(VideoGameID).empty
        numRentals = rentNum(VideoGameID, exist) 
        rentals.append((VideoGameID, numRentals)) 
    
    # Convert to DataFrame for easy sorting 
    sortByRentals = pd.DataFrame(rentals, columns=['VideoGameID', 'rentNum'])

    # Merge rentals with VideoGames DataFrame 
    merge = pd.merge(df2, sortByRentals, on='VideoGameID', how='left')
    merge['rentNum'] = merge['rentNum'].fillna(0) # Fill in no rentals with 0 

    # Sort merged DataFrame by rentNum in descending order
    sortedGames = merge.sort_values(by='rentNum', ascending=False)

    # Print out sorted Games
    print(sortedGames) 
    return sortedGames
# rank

# How many VideoGame IDs are currently active rentals

# How many rentals have there been ever 

# Run
while True: 
    # Note: Add Title input later 
    VideoGameID = input("Enter Video Game ID (V####), 'rank' to see the ranking of Video Games on how often they have been rented out, or 'exit' to quit: ").strip()

    print('\n')

    # Exit the Program    
    if VideoGameID.lower() == 'exit': 
        print("Exiting the program.") 
        break
    # Rank Rentals based on numRentals
    elif VideoGameID.lower() == 'rank': 
        sortedRentals = rank();
        continue

    # Note: Add validation for existent Video Game ID here. 
   
    # Rentals related to inputed VideoGameID
    rentalExist = RentalInfo(VideoGameID) 
    
    # Calculate average Rental Time of said Video Game 
    avgRentalTime(VideoGameID, rentalExist)

    # Calculate how many times said Video Game has been Rented 
    numRentals = rentNum(VideoGameID, rentalExist)
    if numRentals == None: 
        print("No Rentals of this Game have been made.")
    else: 
        print(f"This Video Game has been rented out {numRentals} time(s) before.")
    print('\n')

