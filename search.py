import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def search_all():
    return pd.read_csv('VideoGames.csv')

def search_title(title):
    df = pd.read_csv('VideoGames.csv')
    return df[df['Title'].str.contains(title, case=False, na=False)]

def search_id(id):
    df = pd.read_csv('VideoGames.csv')
    return df[(df['VideoGameID'] == id)]

def search_publisher(publisher):
    df = pd.read_csv('VideoGames.csv')
    return df[df['Publisher'].str.contains(publisher, case=False, na=False)]

def search_year(start_year, end_year):
    df = pd.read_csv('VideoGames.csv')
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
 
def search_available():
    df = pd.read_csv('VideoGames.csv')
    return df[(df['Availability'] == 'Available')].drop(columns='Availability')

@app.route('/search', methods=['POST'])
def output():
    data = request.json
    option = data['option']
    # valid option values are: 'all', 'title', 'id', publisher', 'year', 'availability'
    # idea - frontend javascript should have buttons, properly labelled, and when clicked
    # sends a value to this python program
    # input should be prompted after option is selected
    match option:
            case 'all':
                results = search_all() 
                # no input
            case 'title':
                results = search_title(data.get('input')) 
                # input = title
            case 'id':
                results = search_id(data.get('input')) 
                # input = videogameid
            case 'publisher':
                results = search_publisher(data.get('input')) 
                # input = publisher
            case 'year':
                results = search_year(data.get('first_input'), data.get('second_input'))
                # input = start year (first_input) & end year (second_input)
            case 'available':
                results = search_available()
                # no input
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)