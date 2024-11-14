# This program contains methods that Fetch Specific Details when given ID 

import os
import pandas as pd

# Data Frames 

# Load the .csv files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv')
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv')
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv')

# Read Rentals 
def read_rentals(): 
    return pd.read_csv(RENTAL_PATH)
# read_rentals

# Read Members
def read_members(): 
    return pd.read_csv(MEMBER_PATH)
# read_members

# Read Video Games
def read_games(): 
    return pd.read_csv(VIDEOGAME_PATH)
# read_games

# Fetch Title of corresponding VideoGame based on VideoGameID 
def gameTitle(VideoGameID):
    df = read_games() 

    title = df.loc[df['VideoGameID'] == VideoGameID, 'Title'].values[0]

    return title 
# gameTitle 

# Fetch Name (LastName, FirstName) of corresponding Member based on MemberID
def memberName(MemberID):
    df = read_members()

    first = df.loc[df['MemberID'] == MemberID, 'FirstName'].values[0]
    last = df.loc[df['MemberID'] == MemberID, 'LastName'].values[0]

    name = f"{last}, {first}" 

    return name 
# memberName

# Fetch VideoGameID of corresponding RentalID
def rentalGameID(RentalID):
    df = read_rentals() 

    VideoGameID = df.loc[df['RentalID'] == RentalID, 'VideoGameID'].values[0]

    return VideoGameID 
# rentalGameID 

# Fetch MemberID of corresponding RentalID 
def rentalMemberID(RentalID):
    df = read_rentals() 

    MemberID = df.loc[df['RentalID'] == RentalID, 'MemberID'].values[0] 

    return MemberID
# rentalMemberID
