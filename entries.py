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

# Load CSV file
df = pd.read_csv('Inventory/Rentals.csv')

# Create a DataFrame

# Create a new row (dictionary)
row = {'RentalID': RentalID, 
       'VideoGameID': VideoGameID,
       'MemberID': MemberID, 
       'StartDate': StartDate, 
       'ReturnDate': ReturnDate, 
       'Status': Status}

# Convert dictionary to Data Frame
df = pd.DataFrame.from_dict([row])

# Append new row to CSV file
with open('Inventory/Rentals.csv', 'a', newline='', encoding='utf8') as f: 
  df.to_csv(f, header=False, index=False sep=',')

# df.to_csv('Inventory/Rentals.csv', mode='a', header=False, index=False)

# Display the content of DataFrame
print(df.to_string())
