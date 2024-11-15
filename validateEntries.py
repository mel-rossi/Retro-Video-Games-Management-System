import re
import pandas as pd
from fetchDetails import get_r, get_m, get_g

# This program contains Validation & Generation Methods

# Global Variables 
df_r = get_r() # Rentals DataFrame 
df_m = get_m() # Members DataFrame
df_g = get_g() # (Video) Games DataFrame

# Generate the next valid RentalID 
def generateRentalID():
    
    # Iterate through the column RentalID
    for rentalID in df_r['RentalID']: 
        pass
   
    # Separate the letter and the number 
    letter = rentalID[0]
    number = int(rentalID[1:])

    number += 1 # Next Number 

    return 'R' + format(number, '04') 
# generateRentalID

# Generate the next valid MemberID 
def generateMemberID():

    # Iterate through the column MemberID
    for memberID in df_m['MemberID']: 
        pass
   
    # Separate the letter and the number 
    letter = memberID[0]
    number = int(memberID[1:])

    number += 1 # Next Number 

    return 'M' + format(number, '04') 
# generateMemberID

# Generate the next valid VideoGameID 
def generateVideoGameID():

    # Iterate through the column VideoGameID
    for gameID in df_g['VideoGameID']: 
        pass
   
    # Separate the letter and the number 
    letter = gameID[0]
    number = int(gameID[1:])

    number += 1 # Next Number 

    return 'V' + format(number, '04') 
# generateMemberID
                 
# Check Validation of VideoGameID input 
def validateVideoGameID(VideoGameInput):
    
    # Iterate through the column VideoGameID
    for VideoGameID in df_g['VideoGameID']: 
        if VideoGameID == VideoGameInput: 
            return True 
    
    return False 
# validateVideoGameID

# Confirm if the VideoGameID entered is the correct one 
def confirmVideoGameID(VideoGameInput):

    # Display Video Game information based on ID
    result = df_g[df_g['VideoGameID'] == VideoGameInput]

    return result
# confirmVideoGameID

# Check Validation of MemberID input 
def validateMemberID(MemberInput):

    # Iterate through the column MemberID
    for MemberID in df_m['MemberID']: 
        if MemberInput == MemberID: 
            return True

    return False
# validateMemberID

# Confirm if the MemberID entered is the correct one 
def confirmMemberID(MemberInput):

    # Display Member information based on ID
    result = df_m[df_m['MemberID'] == MemberInput]

    return result
# confirmMemberID

# Check Validation of RentalID input 
def validateRentalID(RentalInput): 

    # Iterate through the column RentalID
    for RentalID in df_r['RentalID']: 
        if RentalInput == RentalID: 
            return True

    return False
# validateRentalID 

# Confirm if the RentalID entered is the correct one 
def confirmRentalID(RentalInput):

    # Display Rental information based on ID
    result = df_r[df_r['RentalID'] == RentalInput]

    return result
# confirmRentalID

# Generate today's date
def generateDate():

    return pd.Timestamp.today().date()
# generateDate

# Check Video Game Availability based on VideoGameID input
def checkAvailability(VideoGameInput): 

    row = df_g[df_g['VideoGameID'] == VideoGameInput] # Find correct Row 

    if not row[row['Availability'] == 'Available'].empty: 
        return True # Available

    return False # Unavailable 
# checkAvailibility

# Check Rental Limit based on MemberID input 
def checkRentalLimit(MemberInput):

    row = df_m[df_m['MemberID'] == MemberInput] # Find correct Row

    if not row[row['CurRentals'] < 5].empty:
        return True # Limit Not Reached

    return False # Limit Reached
# checkRentalLimit

# Check Rental Status based on RentalID input 
def checkRentalStatus(RentalInput):

    row = df_r[df_r['RentalID'] == RentalInput] # Find correct Row

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

