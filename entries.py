import pandas as pd 
 
# Create a DataFrame
df = pd.DataFrame({'RentalID': ['V0072', 'V0136', 'V0655'], 
        'Title': ['Animal Crossing: New Leaf', 'NBA 2K20', 'Need for Speed: Hot Pursuit'], 
        'Publisher': ['Nintendo', '2K Sports', 'Electronic Arts'], 
        'Year': ['2013', '2019', '2010']})

# Write DataFrame to a csv file 
df.to_csv('Inventory/Rentals.csv', index=False)

# Display the content of DataFrame
print(df.to_string())
