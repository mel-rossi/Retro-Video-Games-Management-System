import os
import pandas as pd
from flask_cors import CORS
from flask import request, jsonify, Blueprint

# This program searches through Video Games based on filters indicated through user input

searchgame_bp = Blueprint('SearchGame', __name__)
CORS(searchgame_bp)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')   
CSV_FILE = os.path.join(INVENTORY_DIR, 'VideoGames.csv')

df = pd.read_csv(CSV_FILE)

# Filter Video Games based on input 
def filter_games(title=None, publisher=None, start_year=None, end_year=None, status=None, genre=None):

    filters = pd.Series([True] * len(df), index=df.index)

    # Filters 'Title'
    if title is not None: 
        filters = filters & df['Title'].str.contains(title, case=False, na=False)

    # Filters 'Publisher'
    if publisher is not None: 
        filters = filters & df['Publisher'].str.contains(publisher, case=False, na=False)

    if status is not None: 
        filters = filters & df['Availability'].str.contains(status, case=True, na=False)

    # Filters 'Year'
    if start_year is not None: # based on start_year
        filters = filters & (df['Year'] >= start_year)

    if end_year is not None: # based on end_year 
        filters = filters & (df['Year'] <= end_year) 

    # Filters 'Genre'
    if genre is not None: # based on genre
        # genre input could be an array of genre terms such as ['action', 'adventure', 'shooter', etc...]
        genre = '|'.join(genre)
        filters = filters & df['Genre'].str.contains(genre, case=False, na=False, regex=True)
        # for games with multiple genres, entering one genre will return an entry

    return df[filters]
# filter_games

@searchgame_bp.route('/search_game', methods=['POST'])
def search_game_route():

    data = request.json # Get json data from POST body
    results = filter_games(data.get('title'), data.get('publisher'), data.get('start_year'),
                                     data.get('end_year'), data.get('status'), data.get('genre'))

    return jsonify(results.to_dict(orient='records'))
# search_game_route

