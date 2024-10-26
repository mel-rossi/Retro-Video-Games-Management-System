# This program sorts .CSVs
import os 
import pandas as pd 
from flask_cors import CORS 
from RentalStat import rent_num 
from GameRental import game_filter
from RentalStat import rental_filter
from MemberRental import member_filter
from RentalStat import avg_rental_time
from flask import request, jsonify, Blueprint 

rank_bp = Blueprint('Rank', __name__) 
CORS(rank_bp)

# Load the .csv files 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv') 
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv') 
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv') 

# Read .csv files into DataFrames 
df1 = pd.read_csv(MEMBER_PATH) 
df2 = pd.read_csv(RENTAL_PATH) 
df3 = pd.read_csv(VIDEOGAME_PATH)

# Sort .csv information based on Rental Time (Average Rental Time * Number of Rentals) 
def ranking(idName, filters, df):
    
    # Iterate through DataFrame 
    for ID in df[idName]:
        # Filter rentals for ID 
        rentals = filters(ID) 

        # Calculate numRentals and average rental time 
        numRentals = rent_num(rentals)
        average = avg_rental_time(rentals)

        # Calculate score 
        score = numRentals * average

        # Assign score back to df
        df.loc[df[idName] == ID, 'score'] = score

    # Sort by score 
    df = sort(df, 'score') 

    # Drop 'score' column 
    df = df.drop(columns=['score'])

    return df
# ranking

# Limit amount of ranked output 
def limitOut(df, top):

    df = df.head(top) 

    return df
# limitOut

# Sorts dataframe by valueID
def sort(df, valueID):
    return df.sort_values(by=valueID, ascending=False)
# sort

# Check whether the input for 'base' is valid 
def validBase(base, rank): 
    valid = False 

    if base.lower() == 'id': 
        valid = True 
    elif base.lower() == 'name':
        if rank.lower() == 'member' or rank.lower() == 'game':  
            valid = True
    elif rank.lower() == 'game': 
        if base.lower() == 'year' or base.lower() == 'genre':
            valid = True
 
    return valid
# validBase 

# Process Input
def sortingMethod(rankType, sortBy, top): 

    # Determine the table / .csv to be ranked  

    # Rank Video Games
    if not rankType == None and rankType.lower() == 'game': 
        idName = 'VideoGameID' 
        filters = game_filter
        df = df3
        valueID = 'Title'

    # Rank Members 
    elif not rankType == None and rankType.lower() == 'member': 
        idName = 'MemberID'
        filters = member_filter 
        df = df1
        valueID = 'FirstName'

    # Default = Rank Rentals
    else: 
        idName = 'RentalID'
        filters = rental_filter 
        df = df2

    # Determine what ranking / sorting is based on

    # Default = Sorted by Ranking
    if validBase(sortBy, rankType) == False: 
        ranked = ranking(idName, filters, df) 
    # Other Cases
    else:
        # Rank by ID
        if sortBy.lower() == 'id': 
            ranked = sort(df, idName)

        # Rank by Name = Games : Title / Publisher || Member : First / Last Name 
        elif sortBy.lower() == 'name': 
            ranked = sort(df, valueID)
       
        # Rank Games by Year
        elif sortBy.lower() == 'year': 
            ranked = sort(df, 'Year')

        # Rank Games by Genre 
        elif sortBy.lower() == 'genre': 
            ranked = sort(df, 'Genre') 

    # Limit output

    if top is not None and (isinstance(top, int) or top.isdigit()): 
        if top.isdigit(): 
            top = int(top)

        ranked = limitOut(ranked, top)

    return ranked
# sortingMethod 

@rank_bp.route('/rank', methods=['POST']) 
def rank_route(): 
    data = request.json # Get json data from POST body 
    ranked = sortingMethod(data.get('rank'), data.get('base'), data.get('top'))

    data = { 
        "Ranked": ranked.to_dict(orient='records') 
    } 

    return jsonify(data)
# rank_route
