import pandas as pd 

# Get user input for a value
RentalID = input("Enter Rental ID (make sure not to overwrite an ID, view the last Rental ID first): ")
VideoGameID = input("Enter Video Game ID of Video Game Entered: ")
MemberID = input("Enter Member ID: ")
StartDate = input("Enter Start Date of Rental: ") 
ReturnDate = input("Enter Renturn Date of Rental (leave blank if it hasn't been returned): ")

if ReturnDate == '':
    Status = 'Active'
else:
    Status = 'Inactive'

# Create a DataFrame 
df = pd.DataFrame({'RentalID': [RentalID], 
        'VideoGameID': [VideoGameID], 
        'MemberID': [MemberID], 
        'StartDate': [StartDate],
        'ReturnDate': [ReturnDate], 
        'Status': [Status]})

# Write DataFrame to a csv file 
# currently overwrites the file everytime
f.to_csv('Inventory/Rentals.csv', index=False)

# Display the content of DataFrame
print(df.to_string())
