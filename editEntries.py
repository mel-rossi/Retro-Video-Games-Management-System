# This file allows the user to edit entries in the Rentals table
# For pratical purposes it currently only generates the return date and changes the Status of the Rental 

# Imports
import pandas as pd 
from validateEntries import validateRentalID
from validateEntries import confirmRentalID
from validateEntries import generateDate

df = pd.read_csv('Inventory/Rentals.csv')

# Get RentalID from user input and validate input
validRentalID = False
confirmRental = ""
while confirmRental != "y": # Exits loop when validRentalID == True and confirmRental == "y"
    RentalID = input("Enter the Rental ID of the Rental you would like to mark as returned (R####): ")
    validRentalID = validateRentalID(RentalID)
    if validRentalID == True: 
        confirmRentalID(RentalID)
        confirmRental = input("Enter 'y' if it is correct: ")

# Find value of RentalID and change Return Date and Status to generate today's date and "inactive"
df.loc[df['RentalID'] == RentalID, ['ReturnDate', 'Status']] = [generateDate(), 'Inactive']

# Save updated DataFrame back to CSV file 
df.to_csv('Inventory/Rentals.csv', index=False)

# Display the content of DataFrame
print("This is the updated Rentals: ")
print(df.to_string())
