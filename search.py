import pandas as pd
from flask import Flask, request, jsonify

# WIP!!! 
# this code returns dataframes based off which function is selected
# i think there are a few javascript libraries/frameworks that allow u to display?
# first time using flask please bare with me lol

search = Flask(__name__)

@search.route('/search', methods=['POST'])
def handle_json_requests():
    data = request.json
    option = data.get('option')
    # idea - buttons that are properly labelled should choose option, 
    # search term prompt appears for each option except search_all 
    search_term = data.get('search_term') 
    # valid search terms are: 'all', 'title', 'id', publisher', 'year', 'availability'
    jsonify(select_search(option, search_term)) 
    # if search_all is selected this, value of search_term should not matter & should not be prompted
    # if check_availability is selected, search_term must be id

def select_search(option, search_term):
    match option:
            case 'all':
                return search_all()
            case 'title':
                return search_title(search_term)
            case 'id':
                return search_id(search_term)
            case 'publisher':
                return search_publisher(search_term)
            case 'year':
                return search_year(search_term)
            case 'availability':
                return check_availability(search_term)

def search_all():
    return pd.read_csv('VideoGames.csv')

def search_title(title):
    df = pd.read_csv('VideoGames.csv')
    return df[df['Title'].str.contains(title, case=False, na=False)]

def search_id(id):
    df = pd.read_csv('VideoGames.csv')
    return df[df['VideoGameID'].str.contains(id, case=False, na=False)]

def search_publisher(publisher):
    df = pd.read_csv('VideoGames.csv')
    return df[df['Publisher'].str.contains(publisher, case=False, na=False)]

def search_year(year):
    df = pd.read_csv('VideoGames.csv')
    return df[df['Year'].str.contains(year, case=False, na=False)]
# WIP - year range should be a better option 
def check_availability(id):
    video_games = pd.read_csv('VideoGames.csv')
    rentals = pd.read_csv('Rentals.csv')
    cnt = len(rentals[(rentals['VideoGameID']==id) & rentals['ReturnDate'].isna() & rentals['ReturnDate'].isnull()])
    
    # df1 = pd.DataFrame(data={'Status': ['Available'], 'OutForRent': [cnt], 'MaxStock': []})
    # return if (cnt < video_games.at[1, 'MaxStock']) else return pd.DataFrame
    print(cnt)
# WIP
check_availability('V0001')