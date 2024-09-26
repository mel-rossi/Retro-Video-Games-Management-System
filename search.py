import pandas as pd
from flask import Flask, request, jsonify

# WIP!!! 
# this code returns dataframes based off which function is selected
# i think there are a few javascript libraries/frameworks that allow u to display?
# first time using flask please bare with me lol

search = Flask(__name__)

@search.route('/search', methods=['POST']) #WIP
def handle_json_requests():
    data = request.json
    option = data.get('option')
    # valid option terms are: 'all', 'title', 'id', publisher', 'year', 'availability'
    # idea - javascript should have buttons, properly labelled, and when clicked
    # sends a value to this python program
    search_term = data.get('search_term') 
    jsonify(select_search(option, search_term))
    # if search_all is selected this, value of search_term should not matter & should not be prompted 
    # if search_year is selected, the user should be prompted to enter 2 values (range between years)
    # if check_availability is selected, search_term must be id

def select_search(option, search_term): # WIP
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
                return search_year(search_term) # WIP
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

def search_year(start_year, end_year):
    df = pd.read_csv('VideoGames.csv')
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
 
def check_availability(id):
    video_games = pd.read_csv('VideoGames.csv')
    rentals = pd.read_csv('Rentals.csv')
    max_stock = video_games.loc[video_games['VideoGameID']==id, 'MaxStock'].values[0]
    cnt = len(
        rentals[(rentals['VideoGameID']==id) 
        & rentals['ReturnDate'].isna() & rentals['ReturnDate'].isnull()]
        )
    if (cnt < max_stock):
        status = 'Available'
    else:
        status = 'Unavailable'
    return pd.DataFrame(data={
        'Status': [status], 'AmountAvailable': [max_stock - cnt], 'MaxStock': [max_stock]
        })
    
# if we go with print with python approach:
# print(([insert function]).to_string(index=False))