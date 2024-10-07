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

# Calculate : How many active rentals are there right now? 
def activeRentals(): 
    active = 0

    # Iterate through Status column in Rentals 
    for Status in df1['Status']: 
        if Status == 'Active': 
            active += 1

    print(f"There are currently {active} Active Rentals.\n")
    return active
# activeRentals

# Calculate : How many inactive rentals are there right now? 
def inactiveRentals(): 
    inactive = 0

    # Iterate through Status column in Rentals 
    for Status in df1['Status']:
        if Status == 'Inactive': 
            inactive += 1

    print(f"There are currently {inactive} Inactive Rentals.\n")
    return inactive
# inactiveRentals

# Calculate : How many rentals have the been ever? 
def allRentals(): 
    rentals = 0

    for _, _ in df1.iterrows(): 
        rentals += 1
    
    print(f"There have been {rentals} Rentals in Total thus far.\n")
    return rentals + 1
# allRentals

# Rank Video Games based on number of times they have been rented out
def rank():
    rentals = [] 

    # Iterate through VideoGameID column in Video Games 
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

    # Drop the 'rentNum' column 
    sortedGames = sortedGames.drop(columns=['rentNum'])

    # Print out sorted Games
    print(sortedGames) 
    return sortedGames
# rank

# Run
while True: 
    # Note: Add Title input later 
    VideoGameID = input("Enter one of these:" +  
                "\n\t'V####' (a Video Game ID) to see the Rental History of the Video Game its associated with," + 
                "\n\t'rank' to see the ranking of Video Games based on how often they have been rented out," + 
                "\n\t'active' to find out how many Video Games are currently being rented out," + 
                "\n\t'inactive' to find out how many fulfilled (closed) Rental Transations there have been," + 
                "\n\t'all' to find out how many total Rental Transations there have been" + 
                "\n\t'exit' to quit: ").strip()

    print('\n')

    # Exit the Program    
    if VideoGameID.lower() == 'exit': 
        print("Exiting the program.") 
        break

    # Rank Rentals based on numRentals
    elif VideoGameID.lower() == 'rank': 
        sortedRentals = rank()
        continue

    # Number of active Rentals 
    elif VideoGameID.lower() == 'active': 
        active = activeRentals()
        continue

    # Number of inactive Rentals 
    elif VideoGameID.lower() == 'inactive': 
        inactive = inactiveRentals()
        continue

    elif VideoGameID.lower() == 'all': 
        rentalsEver = allRentals() 
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

