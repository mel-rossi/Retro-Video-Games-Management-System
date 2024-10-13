# This file allows the user to add new entries to the Rentals Table 

# Imports
import pandas as pd
from validateEntries import generateRentalID
from validateEntries import validateVideoGameID
from validateEntries import confirmVideoGameID
from validateEntries import checkAvailability
from validateEntries import validateMemberID
from validateEntries import confirmMemberID
from validateEntries import checkRentalLimit
from validateEntries import generateDate
from linkIDs import rentOut
from linkIDs import incRentals

# Functions

# Get user input for VideoGameID and perform validation checks 
def VideoGameInput(): 
    validGameID = False 
    confirmGameID = "" 
    while confirmGameID != "y": # Exits loop when validGameID == True and available == True 
                                # and confirmGameID == "y" 
        VideoGameID = input("Enter Valid Video Game ID (V####): ") 
        validGameID = validateVideoGameID(VideoGameID)
        if validGameID == True:
            confirmVideoGameID(VideoGameID)
            available = checkAvailability(VideoGameID)
            if (available == True): 
                confirmGameID = input("Enter 'y', if it is correct: ")
        else: 
            print("Invalid VideoGameID. Try Again!")

    return VideoGameID
# VideoGameInput

# Get user input for MemberID and perform validation checks 
def MemberInput():
    validMemberID = False 
    confirmMember = ""
    while confirmMember != "y": # Exits loop when validMemberID == True and limitStat == True 
                                # and confirmGameID == "y"
        MemberID = input("Enter Valid Member ID (M####): ") 
        validMemberID = validateMemberID(MemberID) 
        if validMemberID == True: 
            confirmMemberID(MemberID) 
            limitStat = checkRentalLimit(MemberID)
            if (limitStat == True): 
                confirmMember = input("Enter 'y', if it is correct: ")
        else: 
            print("Invalid MemberID. Try Again!")

    return MemberID
# MemberInput

# Get user input and generate valid values

# Generate the valid next RentalID for the Rental being added
RentalID = generateRentalID()

# Get VideoGameID from user input and validate input 
VideoGameID = VideoGameInput()

# Get MemberID from user input and validate input
MemberID = MemberInput()

# For pratical purposes, generate today's date. 
# As the log would generally be made alongside the Rental,
# therefore on the same date
StartDate = generateDate()

# Return date empty by default, because in practice a entry is made when the rental is checked out. 
# Return date is now generated only when editing a entry with editEntry.py
ReturnDate = ''

Status = 'Active'

# Update dependent columns on files VideoGames.csv and Members.csv
rentOut(VideoGameID)
incRentals(MemberID)

# Read the CSV file into a DataFrame
df = pd.read_csv("Inventory/Rentals.csv")

# Add a new row using loc
row = {'RentalID': RentalID, 
       'VideoGameID': VideoGameID,
       'MemberID': MemberID, 
       'StartDate': StartDate, 
       'ReturnDate': ReturnDate, 
       'Status': Status}

df.loc[len(df)] = row

# Write the updated DataFrame back to the CSV file
df.to_csv("Inventory/Rentals.csv", index=False)

# Display the content of DataFrame
print("This is the updated Rentals: ")
print(df.to_string())
