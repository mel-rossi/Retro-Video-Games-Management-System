# This file allows the user to add new entries to the Rentals Table 

# Imports
import pandas as pd
from validateEntries import generateRentalID
from validateEntries import validateVideoGameID
from validateEntries import validateMemberID

# Get user input for values

# Call generateRentalID
RentalID = generateRentalID()

# Get VideoGameID
validGameID = False
while validGameID == False:
    VideoGameID = input("Enter Valid Video Game ID (V####): ")
    validGameID = validateVideoGameID(VideoGameID)
    
# Get MemberID
validMemberID = False
while validMemberID == False:
    MemberID = input("Enter Valid Member ID (M####): ")
    validMemberID = validateMemberID(MemberID)

StartDate = input("Enter Start Date of Rental: ") 
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
