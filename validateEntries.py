# Validation & Generation Methods 

import pandas as pd

# Data Frames 

# Read Rentals 
df1 = pd.read_csv('Inventory/Rentals.csv')

# Read VideoGames
df2 = pd.read_csv('Inventory/VideoGames.csv')

# Read Members
df3 = pd.read_csv('Inventory/Members.csv')

# Generate the next valid RentalID 
def generateRentalID():
    # Iterate through the column RentalID
    for rentalID in df1['RentalID']: 
        pass
   
    # Separate the letter and the number 
    letter = rentalID[0]
    number = int(rentalID[1:])

    number += 1
    return 'R' + format(number, '04') 
# generateRentalID
                 
# Check Validation of VideoGameID input 
def validateVideoGameID(VideoGameInput): 
    # Iterate through the column VideoGameID
    for VideoGameID in df2['VideoGameID']: 
        if VideoGameID == VideoGameInput: 
            return True 
    
    return False 
# validateVideoGameID

# Confirm if the VideoGameID entered is the correct one 
def confirmVideoGameID(VideoGameInput): 
    # Display Video Game information based on ID
    print("This is the Video Game registration of the corresponding ID: ")
    result = df2.loc[df2.iloc[:, 0] == VideoGameInput]
    print(result)
# confirmVideoGameID

# Check Validation of MemberID input 
def validateMemberID(MemberInput): 
    # Iterate through the column MemberID
    for MemberID in df3['MemberID']: 
        if MemberInput == MemberID: 
            return True

    return False
# validateMemberID

# Confirm if the MemberID entered is the correct one 
def confirmMemberID(MemberInput): 
    # Display Member information based on ID
    print("This is the Member registration of the corresponding ID: ")
    result = df3.loc[df3.iloc[:, 0] == MemberInput] 
    print(result)
# confirmMemberID

# Check Validation of RentalID input 
def validateRentalID(RentalInput): 
    # Iterate through the column RentalID
    for RentalID in df1['RentalID']: 
        if RentalInput == RentalID: 
            return True

    return False
# validateRentalID 

# Confirm if the RentalID entered is the correct one 
def confirmRentalID(RentalInput): 
    # Display Rental information based on ID
    print("This is the Rental registration of the corresponding ID: ")
    result = df1.loc[df1.iloc[:, 0] == RentalInput]
    print(result)
# confirmRentalID

# Generate today's date: YYYY-MM-DD
def generateDate(): 
    return pd.Timestamp.today().date()
# generateDate

# Check Video Game Availability based on VideoGameID input
def checkAvailability(VideoGameInput): 
    row = df2.loc[df2.iloc[:, 0] == VideoGameInput] # Find correct Row 
    if row.iloc[:, -2].eq('Available').any(): # Find the value of the last column : -1 = last column 
                                              # check if said value == 'Available'
        return True # Available 
    print("VideoGame " + VideoGameInput + " is unavailable.")
    return False # Unavailable 
# checkAvailibility

# Check Rental Limit based on MemberID input 
def checkRentalLimit(MemberInput): 
    row = df3.loc[df3.iloc[:, 0] == MemberInput] # Find correct Row 
    if row.iloc[:, -1].item() < 5: # Find if value of last column is less than 5 : -1 = last column 
                                   # check if said value < 5
        return True # Limit Not Reached
    print("Member " + MemberInput + " has reached their Rental Limit(5).")
    return False # Limit Reached
# checkRentalLimit

# Check Rental Status based on RentalID input 
def checkRentalStatus(RentalInput): 
    row = df1.loc[df1.iloc[:, 0] == RentalInput] # Find correct Row
    if row.iloc[:, -1].eq('Active').any(): # Find the value of the last column : -1 = last column
        return True # Active 
    print("Rental " + RentalInput + " is inactive.")
    return False # Inactive
