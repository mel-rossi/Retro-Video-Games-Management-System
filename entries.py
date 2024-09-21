import pandas as pd 

# Get user input for a value
# RentalID = input("Enter Rental ID")


# Create a DataFrame
df = pd.DataFrame({'RentalID': ['0000', '0001', '0002'], 
        'VideoGameID': ['V0055', 'V0090', 'V0140'], 
        'MemberID': ['M0040', 'M0194', 'M0174'], 
        'StartDate': ['08/30/2024', '06/28/2022', '04/16/2020'],
        'ReturnDate': ['', '07/30/2022', '11/02/2021'], 
        'Status': ['Active', 'Inactive', 'Inactive']})

# Write DataFrame to a csv file 
df.to_csv('Inventory/Rentals.csv', index=False)

# Display the content of DataFrame
print(df.to_string())
