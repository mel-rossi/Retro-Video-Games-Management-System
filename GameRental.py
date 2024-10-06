# This program Shows Hisory based off of the Video Game instead of the Member

# BIG WIP

# Imports 
import pandas as pd 
from flask import Flask

app = Flask(__name__) # Define app here 

@app.route('/') # Route Definition 

def hello(): 
    return 'Hello, Word!'

if __name__ == '__main__': 
    app.run(debug=True)

# Data Frames 

# Read Rentals
df1 = pd.read_csv('Inventory/Rentals.csv')

# Read VideoGames 
df2 = pd.read_csv('Inventory/VideoGames.csv')
                           
# Print out Rental Information of VideoGameID

# Calculate average Rental Time (Start - Return Date) 

# How many times VideoGame ID has been rented out 

# Rank based on number of times VideoGames have been rented out 

# How many VideoGame IDs are currently active rentals

# How many rentals have there been ever 

