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
def ranking(idName, filters, df, bias):
    
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
    df = sort(df, 'score', bias) 

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
def sort(df, valueID, bias):
    return df.sort_values(by=valueID, ascending=bias)
# sort

# Check whether the input for 'rank' is valid 
def validRank(rank): 
    valid = False

    if rank is not None and (rank.lower() == 'game' or rank.lower() == 'member'): 
        valid = True

    return valid
# validRank

# Check whether the input for 'base' is valid 
def validBase(base, rank): 
    valid = False 

    if base.lower() == 'id': 
        valid = True 
    elif base.lower() == 'name':
        if validRank(rank):  
            valid = True
    elif rank.lower() == 'game': 
        if base.lower() == 'year' or base.lower() == 'genre':
            valid = True
 
    return valid
# validBase

def validSort(rank, base, sort): 
    valid = False 

    if validBase(base, rank) and sort is not None: 
        if base.lower() == 'name': 
            if rank.lower() == 'game' and sort.lower() == 'publisher': 
                valid = True

            if rank.lower() == 'member' and sort.lower() == 'surname':
                valid = True

        elif base.lower() == 'id': 
            if sort.lower() == 'game' or sort.lower() == 'member': 
                valid = True

    return valid

# validSort 

# Process Input
def sortingMethod(rankType=None, sortBy=None, sortAdd=None, top=None, bias=None):

    # Determine the orientation of the sorting 

    if not bias == None and bias.lower() == 'flip': 
        bias = True
    else: 
        bias = False

    # Determine the table / .csv to be ranked  
    
    if validRank(rankType): 
        # Rank Video Games 
        if rankType.lower() == 'game': 
            idName = 'VideoGameID' 
            filters = game_filter
            df = df3
            valueID = 'Title'

        # Rank Members 
        elif rankType.lower() == 'member': 
            idName = 'MemberID'
            filters = member_filter 
            df = df1
            valueID = 'FirstName'

    # Default = Rank Rentals
    else: 
        idName = 'RentalID'
        filters = rental_filter 
        df = df2

    # Determine additional sorting factors 

    if validSort(rankType, sortBy, sortAdd): 
        # (Rentals) by Video Game ID instead of Rental ID
        if sortAdd.lower() == 'game': 
            idName = 'VideoGameID'

        # (Rentals) by Member ID instead of Rental ID
        elif sortAdd.lower() == 'member': 
            idName = 'MemberID' 

        # (Games) by Publisher instead of Title
        elif sortAdd.lower() == 'publisher': 
            valueID = 'Publisher'

        # (Member) by Last Name instead of First Name
        elif sortAdd.lower() == 'surname': 
            valueID = 'LastName'

    # Determine ranking / sorting to perform 

    # Default = Sorted by Ranking

    if validBase(sortBy, rankType):
        # Sorted by ID
        if sortBy.lower() == 'id': 
            ranked = sort(df, idName, bias)

        # (Games or Members) Sorted by Name / Title 
        elif sortBy.lower() == 'name':
            ranked = sort(df, valueID, bias)
       
        # (Games) Sorted by Year
        elif sortBy.lower() == 'year': 
            ranked = sort(df, 'Year', bias)

        # (Games) Sorted by Genre 
        elif sortBy.lower() == 'genre': 
            ranked = sort(df, 'Genre', bias)
    
    # Default = Sorted by Ranking 
    else:
        ranked = ranking(idName, filters, df)

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
    ranked = sortingMethod(data.get('rank'), data.get('base'), data.get('sort'), 
                           data.get('top'), data.get('trend'))

    data = { 
        "Ranked": ranked.to_dict(orient='records') 
    } 

    return jsonify(data)
# rank_route
