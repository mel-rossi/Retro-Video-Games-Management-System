# This file allows the user to add new entries to the Rentals Table 

# Imports
import pandas as pd
from validateEntries import generateRentalID
from validateEntries import validateVideoGameID
from validateEntries import confirmVideoGameID
from validateEntries import validateMemberID
from validateEntries import confirmMemberID
from validateEntries import generateDate

# Get user input and generate valid values

# Call generateRentalID
RentalID = generateRentalID()

# Get VideoGameID
validGameID = False
confirmGameID = "k"
while confirmGameID != "": # Exits loop when validGameID == True and confirmGameID == ""
    VideoGameID = input("Enter Valid Video Game ID (V####): ")
    validGameID = validateVideoGameID(VideoGameID)
    if validGameID == True:
        confirmVideoGameID(VideoGameID)
        confirmGameID = input("Click enter/return if it is correct: ")
           
# Get MemberID
validMemberID = False
confirmMember = "k"
while confirmMember != "": # Exits loop when validMemberID == True and confirmGameID == ""
    MemberID = input("Enter Valid Member ID (M####): ")
    validMemberID = validateMemberID(MemberID)
    if validMemberID == True:
        confirmMemberID(MemberID)
        confirmMember = input("Click enter/return if it is correct: ")

# For pratical purposes, generate today's date. As the log would generally be made alongside the Rental, therefore on the same date
StartDate = generateDate()

ReturnDate = input("Enter Return Date of Rental (leave blank if it hasn't been returned): ")

if ReturnDate == '':
    Status = 'Active'
else:
    Status = 'Inactive'

# Read the CSV fiel into a DataFrame
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
print(df.to_string())

today_date = pd.Timestamp.today().date()
print(today_date)
