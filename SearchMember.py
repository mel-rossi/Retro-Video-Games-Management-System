import os
import re
import pandas as pd
from validateEntries import validateMemberID
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the .csv file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv')
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv')

members_df = pd.read_csv(MEMBER_PATH)
rentals_df = pd.read_csv(RENTAL_PATH)

# Filter Rental rows where MemberID matches MemberInput 
def filter_rentals(MemberInput): 
    return rentals_df[rentals_df['MemberID'] == MemberInput].copy()
# filter_rentals

# Check whether Rentals of said Member exist
def rental_exist(MemberInput): 
    return not filter_rentals(MemberInput).empty
# rental_exist

# Organize Rental Information of VideoGameID 
def rental_info(MemberInput): 
    # Filter relevant rentals 
    rentals = filter_rentals(MemberInput)

    return rentals
# rental_info

# 
def extract_numbers(phone): 
    return re.sub(r'\D', '', phone)
# extract_numbers

# Search member based on input
def find_member(user_input):
    # Member ID input if only 4 digits
    if user_input.isdigit() and len(user_input) == 4:
        user_input = "M" + user_input

    # Video Game ID input with M + 4 digits 
    elif user_input.startswith("M") and len(user_input) == 5:
        pass

    # Add email input
    # Member Phone Number Or Title
    else:
        # input that has @

        # If input has 10 digits
        if sum(char.isdigit() for char in user_input) == 10: 
            digits = extract_numbers(user_input) # Extract digits 

            user_input = members_df.loc[members_df['PhoneNumber'].apply(extract_numbers) == digits, 'MemberID'].values

        # Invalid Phone Number
        if len(user_input) <= 0:
            return None
        else: 
            user_input = user_input[0]

    # Member ID input validation 
    if validateMemberID(user_input):
        member = members_df[members_df['MemberID'] == user_input]
     
        # Check whether rentals of this MemberID exist 
        exist = rental_exist(user_input) 

        if exist: 
            
            # There is at least one Rental with MemberID 
            rentalData = rental_info(user_input)

            return member, rentalData

        else: 
            return member

    # Invalid MemberID
    else: 
        return None
# find_member

#Flask endpoint to search member

@app.route('/search_member', methods=['POST'])
def search_member_route():
    data = request.json # Get json data from POST body
    user_input = data.get('option') # Extract 'option' field

    member, rentals = find_member(user_input)

    data = {
        "member": member.to_dict(orient='records'),
        "rentals": rentals.to_dict(orient='records')
    }
    
    if not member.empty:
        return jsonify(data)
    else:
        return jsonify ({"error": "No member found with the provided ID or phone number."}), 404
# search_member_route
    
if __name__ == '__main__':
    app.run(debug=True)
