import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the .csv file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
FILE_PATH = os.path.join(INVENTORY_DIR, 'Members.csv')

members_df = pd.read_csv(FILE_PATH)

# Format the member info for output
def member_layout(row):
    return {
        "MemberID": row['MemberID'],
        "FirstName": row['FirstName'],
        "LastName": row['LastName'],
        "PhoneNumber": row['PhoneNumber'],
        "Email": row['Email'],
        "CurRentals": row['CurRentals']
    }
# member_layeout 

# Search member based on input
def find_member(user_input):
    if user_input.isdigit() and len(user_input) == 4:
        user_input = "M" + user_input
    if user_input.startswith("M") and len(user_input) == 5:
        member = members_df[members_df['MemberID'] == user_input]

    # Add email input 
    else: 
        updated_input = user_input.replace("-","").replace(" ", "")
        member = members_df[members_df['PhoneNumber'].str.replace("-","").str.replace(" ","") == updated_input]

    if not member.empty:
        #return member_layout(member.iloc[0])
        return member.iloc[0].astype(object).to_dict()
    else:
        #return jsonify({"error": "No member found with the provided ID or phone number."}), 404
        return None
# find_member

#Flask endpoint to search member

@app.route('/search_member', methods=['POST'])
def search_member_route():
    data = request.json #Get json data from POST body
    user_input = data.get('input') #Extract 'input' field
    member = find_member(user_input)
    
    if member:
        return jsonify(member), 200
        #return jsonify(member.to_dict()), 200
    else:
        return jsonify ({"error": "No member found with the provided ID or phone number."}), 404
# search_member_route
    
if __name__ == '__main__':
    app.run(debug=True)
