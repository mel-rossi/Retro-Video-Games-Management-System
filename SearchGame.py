import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')   
CSV_FILE = os.path.join(INVENTORY_DIR, 'VideoGames.csv')

df = pd.read_csv(CSV_FILE)

def search_games(title, publisher, start_year, end_year, status):
    if (start_year is None or end_year is None):
        return df[df['Title'].str.contains(title, case=False, na=False)
            & (df['Publisher'].str.contains(publisher, case=False, na=False))
            & (df['Availability'].str.contains(status, case=True,na=False))]
    else:
        return df[df['Title'].str.contains(title, case=False, na=False)
            & (df['Publisher'].str.contains(publisher, case=False, na=False))
            & (df['Year'] >= start_year) & (df['Year'] <= end_year)
            & (df['Availability'].str.contains(status, case=True,na=False))]

@app.route('/search_game', methods=['POST'])
def output():
    data = request.json
    results = search_games(data.get('title'), data.get('publisher'), data.get('start_year'),
                                     data.get('end_year'), data.get('status'))
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)