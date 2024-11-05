# This program contains methods that Fetch Specific Details when given ID 

import pandas as pd

# Data Frames 

# Read Rentals 
df1 = pd.read_csv('Inventory/Rentals.csv')

# Read VideoGames
df2 = pd.read_csv('Inventory/VideoGames.csv')

# Read Members
df3 = pd.read_csv('Inventory/Members.csv')

# Fetch Title of corresponding VideoGame based on VideoGameID 
def gameTitle(VideoGameID):

    title = df2.loc[df2['VideoGameID'] == VideoGameID, 'Title'].values[0]

    return title 
# gameTitle 

# Fetch Name (LastName, FirstName) of corresponding Member based on MemberID
def memberName(MemberID): 

    first = df3.loc[df3['MemberID'] == MemberID, 'FirstName'].values[0]
    last = df3.loc[df3['MemberID'] == MemberID, 'LastName'].values[0]

    name = f"{last}, {first}" 

    return name 
# memberName

# Fetch VideoGameID of corresponding RentalID
def rentalGameID(RentalID): 

    VideoGameID = df1.loc[df1['RentalID'] == RentalID, 'VideoGameID'].values[0]

    return VideoGameID 
# rentalGameID 

# Fetch MemberID of corresponding RentalID 
def rentalMemberID(RentalID): 

    MemberID = df1.loc[df1['RentalID'] == RentalID, 'MemberID'].values[0] 

    return MemberID
# rentalMemberID

