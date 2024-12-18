import os
import pandas as pd

# This program contains methods that Fetch Specific Details 

# Load the .csv files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv')
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv')
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv')

# Global DataFrames 
df_r = pd.DataFrame() # Rentals DataFrame 
df_m = pd.DataFrame() # Members DataFrame
df_g = pd.DataFrame() # (Video) Games DataFrame

# Read Rentals 
def read_rentals():

    global df_r
    df_r = pd.read_csv(RENTAL_PATH)
# read_rentals

# Read Members
def read_members(): 

    global df_m
    df_m = pd.read_csv(MEMBER_PATH)
# read_members

# Read Video Games
def read_games():

    global df_g
    df_g = pd.read_csv(VIDEOGAME_PATH)
# read_games

# Initial load of CSV files 
read_rentals() 
read_members() 
read_games()

# Fetch Rentals
def get_r():

    global df_r
    return df_r
# get_r

# Fetch Members 
def get_m(): 

    global df_m
    return df_m
# get_m

# Fetch Video Games 
def get_g(): 

    global df_g 
    return df_g
# get_g


# Write to Rentals 
def write_rentals(df): 

    df.to_csv(RENTAL_PATH, index=False)
# write_rentals

# Write to Members 
def write_members(df): 

    df.to_csv(MEMBER_PATH, index=False) 
# write_members 

# Write to Video Games 
def write_games(df): 

    return df.to_csv(VIDEOGAME_PATH, index=False)
# write_games

# Fetch Title of corresponding VideoGame based on VideoGameID 
def gameTitle(VideoGameID):

    title = df_g.loc[df_g['VideoGameID'] == VideoGameID, 'Title'].values[0]

    return title 
# gameTitle

# Fetch Publisher of corresponding VideoGame based on VideoGameID 
def gamePublisher(VideoGameID): 

    publisher = df_g.loc[df_g['VideoGameID'] == VideoGameID, \
                                'Publisher'].values[0]

    return publisher
# gamePublisher

# Fetch Total Inventory Number of corresponding VideoGame based on VideoGameID
def gameInventory(VideoGameID): 

    inventory = df_g.loc[df_g['VideoGameID'] == VideoGameID, \
                                'Inventory'].values[0]

    return inventory 
# gameInventory

# Fetch Genre(s) of corresponding VideoGame based on VideoGameID 
def gameGenre(VideoGameID): 

    genres = df_g.loc[df_g['VideoGameID'] == VideoGameID, \
                                 'Genre'].values[0]

    return genres
# gameGenre

# Fetch Year of corresponding VideoGame based on VideoGameID 
def gameYear(VideoGameID): 

    year = df_g.loc[df_g['VideoGameID'] == VideoGameID, \
                                'Year'].values[0]

    return year
# gameYear

# Fetch Name (LastName, FirstName) of corresponding Member based on MemberID
def memberName(MemberID):

    first = df_m.loc[df_m['MemberID'] == MemberID, 'FirstName'].values[0]
    last = df_m.loc[df_m['MemberID'] == MemberID, 'LastName'].values[0]

    name = f"{last}, {first}" 

    return name 
# memberName

# Fetch VideoGameID of corresponding RentalID
def rentalGameID(RentalID):

    VideoGameID = df_r.loc[df_r['RentalID'] == RentalID, 'VideoGameID'].values[0]

    return VideoGameID 
# rentalGameID 

# Fetch MemberID of corresponding RentalID 
def rentalMemberID(RentalID):

    MemberID = df_r.loc[df_r['RentalID'] == RentalID, 'MemberID'].values[0] 

    return MemberID
# rentalMemberID
