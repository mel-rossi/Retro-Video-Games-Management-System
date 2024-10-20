# This program sorts .CSVs by
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
def rank(rankType, top):

    # Rank Rentals : default 
    idName = 'RentalID'
    filters = rental_filter
    df = df2

    # Rank Video Games 
    if rankType.lower() == 'game': 
        idName = 'VideoGameID'
        filters = game_filter
        df = df3

    # Rank Members 
    elif rankType.lower() == 'member': 
        idName = 'MemberID' 
        filters = member_filter
        df = df1
    
    # Iterate through DataFrame 
    for ID in df[idName]:
        # Filter rentals for ID 
        rentals = filters(ID) 

        # Calculate numRentals and average rental time 
        numRentals = rent_num(rentals)
        average = avg_rental_time(rentals)

        # Calculate score 
        score = numRentals * average

        # Assign score back to df3
        df.loc[df[idName] == ID, 'score'] = score

        # Sort by score 
        df = df.sort_values(by='score', ascending=False) 

        # Drop 'score' column 
        df = df.drop(columns=['score'])

    # Limit the amount of ranked output 
    if top is not None: 
        df = df.head(top)

    return df

# rank

@rank_bp.route('/rank', methods=['POST']) 
def rank_route(): 
    data = request.json # Get json data from POST body 
    ranked = rank(data.get('rank'), data.get('top'))

    data = { 
        "Ranked": ranked.to_dict(orient='records') 
    } 

    return jsonify(data)
# rank_route
