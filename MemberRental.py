import os
import re
import pandas as pd
from flask_cors import CORS
from flask import request, jsonify, Blueprint 
from validateEntries import validateMemberID

memberrental_bp = Blueprint('MemberRental', __name__)
CORS(memberrental_bp)

# Load the .csv files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv')
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv')
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv')

# Read .csv files into DataFrames 
df1 = pd.read_csv(MEMBER_PATH)
df2 = pd.read_csv(RENTAL_PATH)
df3 = pd.read_csv(VIDEOGAME_PATH)

# Filter Rental rows where MemberID matches MemberInput 
def filter_rentals(MemberInput): 

    return df2[df2['MemberID'] == MemberInput].copy()
# filter_rentals

# Check whether Rentals of said Member exist
def rental_exist(MemberInput):

    return not filter_rentals(MemberInput).empty
# rental_exist

# Grab only 'VideoGameID' and 'Title' from Video Game details
def game_title():

    return df3[['VideoGameID', 'Title']]
# game_title 

# Organize Rental Information of MemberID  
def rental_info(MemberInput):

    # Filter relevant rentals 
    rentals = filter_rentals(MemberInput)

    # Drop the 'MemberID' column
    rentals = rentals.drop(columns=['MemberID'])

    # Retrieve Titles of Video Games  
    titles = game_title()

    # Merge rentals with titles 
    rentals = pd.merge(rentals, titles, on='VideoGameID', how='left')

    # Separate rentals into active and inactive rentals 
    activeRentals = rentals[rentals['Status'] == 'Active'].copy()  
    inactiveRentals = rentals[rentals['Status'] == 'Inactive'].copy()

    # Drop the 'Status' column 
    activeRentals = activeRentals.drop(columns=['Status', 'ReturnDate']) # Additionally drop 'ReturnDate' column 
    inactiveRentals = inactiveRentals.drop(columns=['Status'])

    return activeRentals, inactiveRentals 
# rental_info

# Extract digits from the phone number 
def extract_numbers(phone): 

    return re.sub(r'\D', '', phone)
# extract_numbers

# Process input
def find_member(user_input):
    # Empty DataFrame to return in place of rentals
    empty = pd.DataFrame() 

    # Member ID input if only 4 digits
    if user_input.isdigit() and len(user_input) == 4:
        user_input = "M" + user_input

    # Member ID input with M + 4 digits 
    elif user_input.upper().startswith("M") and len(user_input) == 5 and user_input[1:].isdigit():
        user_input = user_input.upper(); # Case insensitivity: takes care if input starts with "m" instead of "M" 

    # Non MemberID input 
    else:
        # Email input : If input contains '@' 
        if '@' in user_input:
            # Retrieve MemberID associated with Email
            user_input = df1.loc[df1['Email'].str.lower() == user_input.lower(), 'MemberID'].values

        # Phone Number input : If input contains 10 digits
        if sum(char.isdigit() for char in user_input) == 10: 
            digits = extract_numbers(user_input) # Extract digits 

            # Retrieve MemberID associated with Phone Number 
            user_input = df1.loc[df1['PhoneNumber'].apply(extract_numbers) == digits, 'MemberID'].values

        # Invalid Phone Number or Email
        if len(user_input) <= 0:
            return empty, empty, empty

        # Valid Phone Number or Email 
        else: 
            user_input = user_input[0]

    # Member ID input validation 
    if validateMemberID(user_input):
        # Retrieve Member details based on MemberID
        member = df1[df1['MemberID'] == user_input] 

        # Check whether rentals with this MemberID exist 
        exist = rental_exist(user_input) 

        # There is at least one rental with MemberID
        if exist:  
            # Retrive (active & inactive) rentals with this MemberID
            activeRentals, inactiveRentals = rental_info(user_input)

            return member, activeRentals, inactiveRentals

        # No rentals with MemberID
        else:
            return member, empty, empty

    # Invalid MemberID
    else: 
        return empty, empty, empty
# find_member

@memberrental_bp.route('/member_rental', methods=['POST'])
def member_rental_route():

    data = request.json # Get json data from POST body
    user_input = data.get('option') # Extract 'option' field

    member, activeRentals, inactiveRentals = find_member(user_input)

    data = {
        "member": member.to_dict(orient='records'),
        "active rentals": activeRentals.to_dict(orient='records'),
        "inactive rentals": inactiveRentals.to_dict(orient='records')
    }
   
    # Valid Input 
    if not member.empty:
        return jsonify(data)

    # Invalid Input 
    else:
        return jsonify ({"error": "No member found with the provided ID, phone number, or email."}), 404
# search_member_route
    
if __name__ == '__main__':
    app.run(debug=True)
