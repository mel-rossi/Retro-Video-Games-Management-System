# Validation & Valid Generation methods 
# Currently a Work In Progress
import pandas as pd

# Data Frames 

# Read Rentals 
df1 = pd.read_csv('Inventory/Rentals.csv')

# Read VideoGames
df2 = pd.read_csv('Inventory/VideoGames.csv')

# Read Members
df3 = pd.read_csv('Inventory/Members.csv')
 
def generateRentalID():
    # Iterate through the column RentalID
    for rentalID in df1['RentalID']: 
        pass

    return rentalID + 1
# generateRentalID()

def validateVideoGameID(VideoGameInput): 
    # Iterate through the column VideoGameID
    for VideoGameID in df2['VideoGameID']: 
        if VideoGameID == VideoGameInput: 
            return True 
    
    print("Invalid VideoGameID. Try Again!")
    return False 
# validateVideoGameID

def validateMemberID(MemberInput): 
    # Iterate through the column MemberID
    for MemberID in df3['MemberID']: 
        if MemberInput == MemberID: 
            return True

    print("Invalid MemberID. Try Again!")
    return False
# validateMemberID

def generateDate(): 
    return pd.Timestamp.today().date()
# generateDate
