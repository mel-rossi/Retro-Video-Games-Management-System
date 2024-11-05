import os 
import pandas as pd
from flask_cors import CORS
from linkIDs import rentOut, incRentals
from flask import request, jsonify, Blueprint, session
from validateEntries import generateDate, generateRentalID
from validateEntries import confirmMemberID, validateMemberID
from validateEntries import checkRentalLimit, checkAvailability
from validateEntries import confirmVideoGameID, validateVideoGameID

# This file allows the user to add new entries to the Rentals Table

addrental_bp = Blueprint('AddRental', __name__)
CORS(addrental_bp)
addrental_bp.secret_key = 'supersecretkey' # Session Management 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
CSV_FILE = os.path.join(INVENTORY_DIR, 'Rentals.csv')

# Dry Run : Initial Input Validation 
def dry_run_entry(VideoGameID, MemberID): 
    
    # Validate VideoGameID 
    if not validateVideoGameID(VideoGameID): 
        return jsonify({ "error": "Invalid Video Game ID" }), 400

    if not checkAvailability(VideoGameID): 
        return jsonify({ "error": "Video game is not available" }), 400 

    # Validate MemberID 
    if not validateMemberID(MemberID): 
        return jsonify({ "error": "Invalid Member ID" }), 400

    if not checkRentalLimit(MemberID): 
        return jsonify({ "error": "Rental limit reached for this member" }), 400

    session['VideoGameID'] = VideoGameID 
    session['MemberID'] = MemberID

    return jsonify({
        "Video Game Registration": confirmVideoGameID(VideoGameID).to_dict(orient='records'), 
        "Member Registration": confirmMemberID(MemberID).to_dict(orient='records'),
        "Message": "Please confirm the details"
    }), 200

# dry_run_entry

# Primary Validation : Process Input and perform modification if appropriate 
def add_entry(VideoGameID, MemberID):

    # Primary Validation 
    if not validateVideoGameID(VideoGameID) or not checkAvailability(VideoGameID) or not validateMemberID(MemberID) or not checkRentalLimit(MemberID):
           return jsonify({"error": "Primary Validation Failed!"})

    # Generate the valid next RentalID for the Rental being added
    RentalID = generateRentalID() 

    # Generate today's date as StartDate 
    StartDate = generateDate()
    StartDate = StartDate.strftime('%Y-%m-%d') # Format it 

    # Return date empty (-1) by default 
    ReturnDate = '-1' 

    Status = 'Active' 

    # Update dependent columns on files VideoGames.csv and Members.csv 
    rentOut(VideoGameID) 
    incRentals(MemberID) 

    # Read CSV file into a DataFrame 
    df = pd.read_csv(CSV_FILE) 

    # Make a new row (registration) 
    row = { 'RentalID': RentalID, 
            'VideoGameID': VideoGameID,
            'MemberID': MemberID, 
            'StartDate': StartDate, 
            'ReturnDate': ReturnDate, 
            'Status': Status
    }
    
    row = pd.DataFrame(row, index=[0]) # convert to Data Frame

    df = pd.concat([df, row], ignore_index=True) 

    # Write the updated DataFrame back to the CSV file 
    df.to_csv(CSV_FILE, index=False) 

    # Return the updated DataFrame as JSON 
    return jsonify(df.to_dict(orient='records')), 200
# add_entry

@addrental_bp.route('/add_rentals', methods=['POST']) 
def add_rental_route(): 

    data = request.json # Get json data from POST body 

    # Dry Run: Initial validation and confirmation 
    if 'Confirm' not in data: 
        return dry_run_entry(data.get('VideoGameID'), data.get('MemberID'))

    # Confirm: Primary validation and prooceed with adding entry if appropriate 
    if data.get('Confirm').lower() == 'confirmed':
        VideoGameID = session.get('VideoGameID') 
        MemberID = session.get('MemberID') 
        return add_entry(VideoGameID, MemberID) 
    else: 
        return jsonify({"message": "Operation cancelled"}), 200
# add_rental_route
