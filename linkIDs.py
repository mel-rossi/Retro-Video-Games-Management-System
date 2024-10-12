# Methods that link and work with columns in different tables that are dependent on each other 

# Imports 
import pandas as pd

# Read VideoGames 
df1 = pd.read_csv('Inventory/VideoGames.csv')

# Read Members
df2 = pd.read_csv('Inventory/Members.csv')

# Read Rentals
df3 = pd.read_csv('Inventory/Rentals.csv')

def instanceNum(VideoGameInput): 
    # Instances of VideoGameInput when Status is Active 
    rentals = df3.loc[(df3['VideoGameID'] == VideoGameInput] & (df3['Status'] == 'Active')]

    # Number of instances
    rentals = len(rentals)

    return rentals
# instanceNum

# Change VideoGame Availability to 'Unavailable'
def rentOut(VideoGameInput):

    # Check how many copies of VideoGameID are rented out
    rentalInstance = instanceNum(VideoGameInput)

    # Check if Active Rental Instances are the same as the Inventory Number 
    if not df1.loc[(df1['VideoGameID' == VideoGameInput] & 'Inventory' == rentalInstance + 1)].empty: 
        # Find the value of VideoGameID and change Availability to Unavailable 
        df1.loc[df1['VideoGameID']== VideoGameInput, 'Availability'] = 'Unavailable'

        # Save update DataFrame back to CSV file 
        df1.to_csv('Inventory/VideoGames.csv', index=False)
# rentOut

# Change VideoGame Availability to 'Available'
def returnGame(VideoGameInput): 

    # Check how many copies of VideoGameID are rented out 
    rentalInstance = instanceNum(VideoGameInput) 

    # Check if Active Rental Instances are less than the Inventory Number
    if not df1.loc[(df1['VideoGameID' = VideoGameIDInput] & 'Inventory' <= rentalInstance)].empty: 
        # Find the value of VideoGameID and change Availability to Available    
        df1.loc[df1['VideoGameID'] == VideoGameInput, 'Availability'] = 'Available'

        # Save updated DataFrame back to CSV file
        df1.to_csv('Inventory/VideoGames.csv', index=False)
# returnGame

# Increase Number of Active Rentals a Member has 
def incRentals(MemberInput): 
    # Increments number of active rentals a Member has 
    df2.loc[df2['MemberID'] == MemberInput, 'CurRentals'] += 1

    # Save updated DataFrame back to CSV file
    df2.to_csv('Inventory/Members.csv', index=False)
# incRentals 

# Decrease Number of Active Rentals a Member has 
def decRentals(MemberInput): 
    # Decrements number of active rentals a Member has 
    df2.loc[df2['MemberID'] == MemberInput, 'CurRentals'] -= 1

    # Save updated DataFrame back to CSV file
    df2.to_csv('Inventory/Members.csv', index=False)
# decRentals
