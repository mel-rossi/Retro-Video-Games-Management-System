# This program contains Validation & Generation Methods 

import re
import pandas as pd
from fetchDetails import read_rentals
from fetchDetails import read_games
from fetchDetails import read_members

# Generate the next valid RentalID 
def generateRentalID():
    
    df = read_rentals() # Read Rentals into DataFrame

    # Iterate through the column RentalID
    for rentalID in df['RentalID']: 
        pass
   
    # Separate the letter and the number 
    letter = rentalID[0]
    number = int(rentalID[1:])

    number += 1 # Next Number 

    return 'R' + format(number, '04') 
# generateRentalID

# Generate the next valid MemberID 
def generateMemberID():

    df = read_members() # Read Members to DataFrame
    
    # Iterate through the column MemberID
    for memberID in df['MemberID']: 
        pass
   
    # Separate the letter and the number 
    letter = memberID[0]
    number = int(memberID[1:])

    number += 1 # Next Number 

    return 'M' + format(number, '04') 
# generateMemberID

# Generate the next valid VideoGameID 
def generateVideoGameID():

    df = read_games() # Read Video Games to DataFrame

    # Iterate through the column VideoGameID
    for gameID in df['VideoGameID']: 
        pass
   
    # Separate the letter and the number 
    letter = gameID[0]
    number = int(gameID[1:])

    number += 1 # Next Number 

    return 'V' + format(number, '04') 
# generateMemberID
                 
# Check Validation of VideoGameID input 
def validateVideoGameID(VideoGameInput):
    
    df = read_games() # Read VideoGames into DataFrame 

    # Iterate through the column VideoGameID
    for VideoGameID in df['VideoGameID']: 
        if VideoGameID == VideoGameInput: 
            return True 
    
    return False 
# validateVideoGameID

# Confirm if the VideoGameID entered is the correct one 
def confirmVideoGameID(VideoGameInput):

    df = read_games() # Read Video Games into DataFrame

    # Display Video Game information based on ID
    result = df[df['VideoGameID'] == VideoGameInput]

    return result
# confirmVideoGameID

# Check Validation of MemberID input 
def validateMemberID(MemberInput):

    df = read_members() # Read Members to DataFrame

    # Iterate through the column MemberID
    for MemberID in df['MemberID']: 
        if MemberInput == MemberID: 
            return True

    return False
# validateMemberID

# Confirm if the MemberID entered is the correct one 
def confirmMemberID(MemberInput):

    df = read_members() # Read Members to DataFrame

    # Display Member information based on ID
    result = df[df['MemberID'] == MemberInput]

    return result
# confirmMemberID

# Check Validation of RentalID input 
def validateRentalID(RentalInput): 

    df = read_rentals() # Read Rentals to DataFrame

    # Iterate through the column RentalID
    for RentalID in df['RentalID']: 
        if RentalInput == RentalID: 
            return True

    return False
# validateRentalID 

# Confirm if the RentalID entered is the correct one 
def confirmRentalID(RentalInput):

    df = read_rentals() # Read Rentals to DataFrame 

    # Display Rental information based on ID
    result = df[df['RentalID'] == RentalInput]

    return result
# confirmRentalID

# Generate today's date
def generateDate():

    return pd.Timestamp.today().date()
# generateDate

# Check Video Game Availability based on VideoGameID input
def checkAvailability(VideoGameInput): 

    df = read_games() # Read Video Games to DataFrame

    row = df[df['VideoGameID'] == VideoGameInput] # Find correct Row 

    if not row[row['Availability'] == 'Available'].empty: 
        return True # Available

    return False # Unavailable 
# checkAvailibility

# Check Rental Limit based on MemberID input 
def checkRentalLimit(MemberInput):

    df = read_members() # Read Members to DataFrame

    row = df[df['MemberID'] == MemberInput] # Find correct Row

    if not row[row['CurRentals'] < 5].empty:
        return True # Limit Not Reached

    return False # Limit Reached
# checkRentalLimit

# Check Rental Status based on RentalID input 
def checkRentalStatus(RentalInput):

    df = read_rentals() # Read Rentals to DataFrame 

    row = df[df['RentalID'] == RentalInput] # Find correct Row
    if not row[row['Status'] == 'Active'].empty:         
        return True # Active

    return False # Inactive
# checkRentalStatus

def validateStringFormat(pattern, string):

    if not isinstance(string, str): 
        return False

    if re.match(pattern, string): 
        return True
    else: 
        return False
# validateStringFormat 

# Check Whether the Name is in a valid format 
def validateNameFormat(Name): 
    
    pattern = r'^(?! )[A-Z][a-z]*(?: [A-Z][a-z]*)*$'

    return validateStringFormat(pattern, Name) 
# checkNameFormat

# Check Whether the Phone Number is in valid format 
def validatePhoneFormat(Phone):

    pattern = r'^\d{3}-\d{3}-\d{4}$'
    
    return validateStringFormat(pattern, Phone) 

# validatePhoneFormat

# Check Whether the Email is in valid format 
def validateEmailFormat(Email):

    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

    return validateStringFormat(pattern, Email) 

# validateEmail

