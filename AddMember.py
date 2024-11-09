import os 
import pandas as pd 
from flask_cors import CORS
from validateEntries import generateMemberID
from validateEntries import validateNameFormat
from validateEntries import validateEmailFormat
from validateEntries import validatePhoneFormat
from flask import request, jsonify, Blueprint, session 

# This file allows the use to add new entries to the Members Tablle 

addmember_bp = Blueprint('AddMember', __name__)
CORS(addmember_bp) 
addmember_bp.secret_key = 'supersecretkey' # Session Management 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
CSV_FILE = os.path.join(INVENTORY_DIR, 'Members.csv') 

# Dry Run : Initial Input Validation 
def dry_run_add_member(FirstName, LastName, PhoneNumber, Email):

    # Validate FirstName & LastName 
    if FirstName is None: 
        return jsonify({"error": "First Name Missing"}), 400

    if LastName is None: 
        return jsonify({"error": "Last Name Missing"}), 400

    if not validateNameFormat(FirstName) or not validateNameFormat(LastName): 
        return jsonify({"error": "Invalid Name Format"}), 400

    # Validate PhoneNumber
    if PhoneNumber is None: 
        return jsonify({"error": "Phone Number Missing"}), 400

    if not validatePhoneFormat(PhoneNumber): 
        return jsonify({"error": "Invalid Phone Number Format"}) 

    # Validate Email
    if Email is None: 
        return jsonify({"error": "Email Missing"}), 400

    if not validateEmailFormat(Email): 
        return jsonify({"error": "Invalid Email Format"}), 400

    session['FirstName'] = FirstName
    session['LastName'] = LastName 
    session['PhoneNumber'] = PhoneNumber 
    session['Email'] = Email

    return jsonify({
        "First Name Entered": FirstName, 
        "Last Name Entered": LastName,
        "Phone Number Entered": PhoneNumber, 
        "Email Entered": Email,  
        "Message": "Please confirm the details"
    }), 200

# dry_run_add_member

# Primary Validation : Process Input and perform modification if appropriate 
def add_member(FirstName, LastName, PhoneNumber, Email): 

    # Primary Validation
    if not validateNameFormat(FirstName) or not validateNameFormat(LastName) or not validatePhoneFormat(PhoneNumber) or not validateEmailFormat(Email): 
        return jsonify({"error": "Primary Validation Failed!"})

    # Generate the valid next MemberID for the Member being added 
    MemberID = generateMemberID() 

    # Set Number of Current Rentals to 0 
    CurRentals = 0 

    # Read CSV file into a DataFrame 
    df = pd.read_csv(CSV_FILE)

    # Make a new row (registration) 
    row = { 'MemberID': MemberID, 
            'FirstName': FirstName, 
            'LastName': LastName, 
            'PhoneNumber': PhoneNumber, 
            'Email': Email, 
            'CurRentals': CurRentals
    }

    row = pd.DataFrame(row, index=[0]) # convert to DataFrame 

    df = pd.concat([df, row], ignore_index=True) 

    # Write the updated DataFram back to the CSV file 
    df.to_csv(CSV_FILE, index=False)

    # Return the updated row as JSON 
    return jsonify({"Registration Added": row.to_dict(orient='records')}), 200

# add_member 

@addmember_bp.route('/add_member', methods=['POST']) 
def add_member_route(): 

    data = request.json # Get json data from POST body 

    # Dry Run: Initial validation and confirmation 
    if 'Confirm' not in data: 
        return dry_run_add_member(data.get('FirstName'), 
                                  data.get('LastName'), 
                                  data.get('PhoneNumber'), 
                                  data.get('Email')) 

    # Confirm: Primary validation and prooceed with adding entry if appropriate
    if data.get('Confirm').lower() == 'confirmed': 
        FirstName = session.get('FirstName')
        LastName = session.get('LastName') 
        PhoneNumber = session.get('PhoneNumber') 
        Email = session.get('Email') 
        return add_member(FirstName, LastName, PhoneNumber, Email)

    else: 
        return jsonify({"message": "Operation cancelled"}), 200 

# add_member_route
