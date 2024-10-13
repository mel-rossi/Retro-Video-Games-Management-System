import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')   
CSV_FILE = os.path.join(INVENTORY_DIR, 'VideoGames.csv') 

def search_all():
    return pd.read_csv(CSV_FILE)

def search_title(title, status):
    df = pd.read_csv(CSV_FILE)
    return df[df['Title'].str.contains(title, case=False, na=False) & (df['Availability'].str.contains(status, case=True,na=False))]

def search_id(id, status):
    df = pd.read_csv(CSV_FILE)
    return df[(df['VideoGameID'] == id) & (df['Availability'].str.contains(status, case=True,na=False))]

def search_publisher(publisher, status):
    df = pd.read_csv(CSV_FILE)
    return df[df['Publisher'].str.contains(publisher, case=False, na=False) & (df['Availability'].str.contains(status, case=True,na=False))]

def search_year(start_year, end_year, status):
    df = pd.read_csv(CSV_FILE)
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Availability'].str.contains(status, case=True,na=False))]
 
def search_available():
    df = pd.read_csv(CSV_FILE)
    return df[(df['Availability'] == 'Available')].drop(columns='Availability')

def search_general(title, publisher, start_year, end_year, status):
    df = pd.read_csv(CSV_FILE)

    if (start_year is None or end_year is None):
        return df[df['Title'].str.contains(title, case=False, na=False)
            & (df['Publisher'].str.contains(publisher, case=False, na=False))
            & (df['Availability'].str.contains(status, case=True,na=False))]
    else:
        return df[df['Title'].str.contains(title, case=False, na=False)
            & (df['Publisher'].str.contains(publisher, case=False, na=False))
            & (df['Year'] >= start_year) & (df['Year'] <= end_year)
            & (df['Availability'].str.contains(status, case=True,na=False))]


@app.route('/search', methods=['POST'])
def output():
    data = request.json
    option = data.get('option')
    
    match option:
        case 'all':
            results = search_all() 
        case 'title':
            results = search_title(data.get('first_input'), data.get('status')) 
        case 'id':
            results = search_id(data.get('first_input'), data.get('status')) 
        case 'publisher':
            results = search_publisher(data.get('first_input'), data.get('status')) 
        case 'year':
            results = search_year(data.get('first_input'), data.get('second_input'), data.get('status'))
        case 'available':
            results = search_available()
        case 'all_params':
            results = search_general(data.get('title'), data.get('publisher'), data.get('start_year'),
                                     data.get('end_year'), data.get('status'))
            
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
