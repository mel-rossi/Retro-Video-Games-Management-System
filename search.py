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
    return df[df['Title'].str.contains(title, case=False, na=False) & (df['Availability'] == status)]

def search_id(id, status):
    df = pd.read_csv(CSV_FILE)
    return df[(df['VideoGameID'] == id) & (df['Availability'] == status)]

def search_publisher(publisher, status):
    df = pd.read_csv(CSV_FILE)
    return df[df['Publisher'].str.contains(publisher, case=False, na=False) & (df['Availability'] == status)]

def search_year(start_year, end_year, status):
    df = pd.read_csv(CSV_FILE)
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year) & (df['Availability'] == status)]
 
def search_available():
    df = pd.read_csv(CSV_FILE)
    return df[(df['Availability'] == 'Available')].drop(columns='Availability')

@app.route('/search', methods=['POST'])
def output():
    data = request.json
    option = data['option']
    
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
    
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)