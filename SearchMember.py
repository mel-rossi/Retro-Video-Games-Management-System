import pandas as pd 
from flask_cors import CORS 
from fetchDetails import get_m
from MemberRental import extract_numbers
from flask import request, jsonify, Blueprint

# This programs searches though Members based on filters indicated through user input 

# Blueprint
searchmember_bp = Blueprint('SearchMember', __name__) 
CORS(searchmember_bp) 

# Global Variables 
df = get_m() # Members DataFrame

# Filter Members based on input 
def filter_members(firstName=None, lastName=None, phone=None, email=None, limit=None):

    filters = pd.Series([True] * len(df), index=df.index)

    # Filters 'First Name' 
    if firstName is not None: 
        filters = filters & df['FirstName'].str.contains(firstName, case=False, na=False) 

    # Filters 'Last Name' 
    if lastName is not None: 
        filters = filters & df['LastName'].str.contains(lastName, case=False, na=False) 

    # Filters 'Phone Number' 
    if phone is not None:
        if phone.isdigit(): 
            filters = filters & df['PhoneNumber'].apply(extract_numbers).str.contains(phone) 
        else: 
            filters = filters & df['PhoneNumber'].str.contains(phone, case=False, na=False) 

    # Filters 'Email' 
    if email is not None: 
        filters = filters & df['Email'].str.contains(email, case=False, na=False) 

    # Filters 'Limit Reached or Not' 
    if limit is not None:
        if limit.lower() == 'reached': 
            filters = filters & (df['CurRentals'] == 5)
        elif limit.lower() == 'not':
            filters = filters & (df['CurRentals'] < 5)

    return df[filters]
# filter_members

@searchmember_bp.route('/search_member', methods=['POST']) 
def search_member_route():

    # Update global DataFrame
    global df 
    df = get_m()

    data = request.json # Get json data from POST body 
    results = filter_members(data.get('forename'), data.get('surname'), data.get('phone'), data.get('email'), data.get('limit')) 

    return jsonify(results.to_dict(orient='records')) 
