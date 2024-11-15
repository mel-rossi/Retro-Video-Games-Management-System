import pandas as pd
from flask_cors import CORS
from fetchDetails import get_g
from flask import request, jsonify, Blueprint

# This program searches through Video Games based on filters indicated through user input

# Blueprint 
searchgame_bp = Blueprint('SearchGame', __name__)
CORS(searchgame_bp)

# Global Variables 
df = get_g() # (Video) Games DataFrame 

# Filter Video Games based on input 
def filter_games(title=None, publisher=None, start_year=None, end_year=None, status=None, genre=None):

    filters = pd.Series([True] * len(df), index=df.index)

    # Filters 'Title'
    if title is not None: 
        filters = filters & df['Title'].str.contains\
                (title, case=False, na=False)

    # Filters 'Publisher'
    if publisher is not None: 
        filters = filters & df['Publisher'].str.contains\
                (publisher, case=False, na=False)

    # Filters 'Availability'
    if status is not None: 
        filters = filters & df['Availability'].str.contains\
                (status, case=True, na=False)

    # Filters 'Year'
    if start_year is not None: # based on start_year
        filters = filters & (df['Year'] >= start_year)

    if end_year is not None: # based on end_year 
        filters = filters & (df['Year'] <= end_year) 

    # Filters 'Genre'
    if genre is not None: # based on genre
        # genre input NEEDS to an array of genre terms such as 
        # ['action', 'adventure', 'shooter', etc...]
        # applies even if it is just one genre term
        genre = '|'.join(genre)
        filters = filters & df['Genre'].str.contains\
                (genre, case=False, na=False, regex=True)
        # for games with multiple genres, entering 
        # one genre will return entries with that contain that genre

    return df[filters]
# filter_games

def sort_by_rank(results):

    # Sort initial df by rank
    results.sort_values(by='Rank', ascending=True, inplace=True)

    # Prevents unnecessary calculations if we want all games sorted by rank
    if len(df) != len(results): 
        # Ovewrite existing rank column values
        results['Rank'] = range(1, len(results) + 1) 

    return results
# sort_by_rank

@searchgame_bp.route('/search_game', methods=['POST'])
def search_game_route():

    data = request.json # Get json data from POST body
    results = filter_games(data.get('title'), data.get('publisher'), \
                        data.get('start_year'), data.get('end_year'), \
                        data.get('status'), data.get('genre'))
    
    # if parameter 'ranked' is not none (it can be anything else), then sort result by rank
    if (data.get('ranked') is not None): 
        results = sort_by_rank(results)

    return jsonify(results.to_dict(orient='records'))
# search_game_route

