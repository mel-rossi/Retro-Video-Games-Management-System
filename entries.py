# This file allows the user to add new entries to the Rentals Table 

# Imports
import pandas as pd
from validateEntries import generateRentalID
from validateEntries import validateVideoGameID
from validateEntries import confirmVideoGameID
from validateEntries import validateMemberID
from validateEntries import generateDate

# Get user input and generate valid values

# Call generateRentalID
RentalID = generateRentalID()

# Get VideoGameID
validGameID = False
confirmGameID = "k"
while True:
    VideoGameID = input("Enter Valid Video Game ID (V####): ")
    validGameID = validateVideoGameID(VideoGameID)
    if validGameID == True:
        confirmVideoGameID(VideoGameID)
        confimGameID = input("Click enter/return if it is correct: ")
        if confirmGameID == "":
            break
        break
           
# Get MemberID
validMemberID = False
while validMemberID == False:
    MemberID = input("Enter Valid Member ID (M####): ")
    validMemberID = validateMemberID(MemberID)

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
