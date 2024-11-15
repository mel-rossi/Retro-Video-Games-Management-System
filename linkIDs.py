# Methods that link and work with columns in different tables that are dependent on each other 

# Imports 
import pandas as pd
from fetchDetails import get_r, get_m, get_g

# Global Variables 
df_r = get_r() # Rentals DataFrame
df_m = get_m() # Members DataFrame
df_g = get_g() # (Video) Games DataFrame

# How many copies of a Video Game are currently rented out
def instanceNum(VideoGameInput):

    # Instances of VideoGameInput when Status is Active 
    rentals = df_r.loc[(df_r['VideoGameID'] == VideoGameInput) \
                     & (df_r['Status'] == 'Active')]

    # Number of instances
    rentals = len(rentals)

    return rentals
# instanceNum

# Change VideoGame Availability to 'Unavailable'
def rentOut(VideoGameInput):

    # Check how many copies of VideoGameID are rented out
    rentalInstance = instanceNum(VideoGameInput)

    # Check if Active Rental Instances are the same as the Inventory Number 
    if not df_g.loc[(df_g['VideoGameID'] == VideoGameInput) \
                & (df_g['Inventory'] == rentalInstance + 1)].empty:

        # Find the value of VideoGameID and change Availability to Unavailable 
        df_g.loc[df_g['VideoGameID'] == VideoGameInput, 'Availability'] \
                                                  = 'Unavailable'

        # Save updated DataFrame back to CSV file 
        write_games(df_g)
# rentOut

# Change VideoGame Availability to 'Available'
def returnGame(VideoGameInput):
    
    # Check how many copies of VideoGameID are rented out 
    rentalInstance = instanceNum(VideoGameInput) 

    # Check if Active Rental Instances are less than the Inventory Number
    if not df_g.loc[(df_g['VideoGameID'] == VideoGameInput) \
                  & (df_g['Inventory'] <= rentalInstance)].empty:

        # Find the value of VideoGameID and change Availability to Available    
        df_g.loc[df_g['VideoGameID'] == VideoGameInput, 'Availability'] \
                                                      = 'Available'

        # Save updated DataFrame back to CSV file
        write_games(df_g)
# returnGame

# Increase Number of Active Rentals a Member has 
def incRentals(MemberInput):
    
    # Increments number of active rentals a Member has 
    df_m.loc[df_m['MemberID'] == MemberInput, 'CurRentals'] += 1

    # Save updated DataFrame back to CSV file
    write_members(df_m)
# incRentals 

# Decrease Number of Active Rentals a Member has 
def decRentals(MemberInput):

    # Decrements number of active rentals a Member has 
    df_m.loc[df_m['MemberID'] == MemberInput, 'CurRentals'] -= 1

    # Save updated DataFrame back to CSV file
    write_members(df_m)
# decRentals
