import pandas as pd 

# Read the Excel file 
# df = pd.read_excel("Inventory.xlsx")

# Convert the DataFrame to a CSV string 
# csv_data = df.to_csv(index=False)

# Read a csv file using Pandas 
df = pd.read_csv("Inventory/Rentals.csv")

# Write to a csv file using Pandas 
# df.to_cvs("output_file.csv", index=False)

# You can now work with the csv_data string
# print(cvs_data)

print(df.to_string()) 

// This program currently prints out the Rentals table. 
