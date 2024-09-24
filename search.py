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
    search_term = data.get('search_term') # valid search terms are: 'all', 'title', 'id', 'publisher', 'year'
    select_search(option, search_term) # if search_all is selected this, value of search_term should not matter

def select_search(option, search_term): # note: i need to jsonify
    match option:
            case 'all':
                return search_all()
            case 'available':
                return search_available(search_term)
            case 'title':
                return search_title(search_term)
            case 'id':
                return search_id(search_term)
            case 'publisher':
                return search_publisher(search_term)
            case 'year':
                return search_year(search_term)

def search_all():
    return pd.read_csv('VideoGames.csv')

def search_available():
    return('test')
# WIP - i need to compare entries in rentals table for this to work

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