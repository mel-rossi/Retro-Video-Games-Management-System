import os
import pandas as pd
from flask_cors import CORS
from linkIDs import returnGame, decRentals
from flask import request, jsonify, Blueprint, session
from validateEntries import generateDate, confirmRentalID
from validateEntries import validateRentalID, checkRentalStatus

# This file allows the user to close Rental Transactions (Registration --> Status => "Inactive") 

closerental_bp = Blueprint('CloseRental', __name__)
CORS(closerental_bp)
closerental_bp.secret_key = 'supersecretkey' # Session Management

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
CSV_FILE = os.path.join(INVENTORY_DIR, 'Rentals.csv')

# Dry Run : Initial Input Validation
def dry_run_close_entry(RentalID): 

    # Validate RentalID 
    if not validateRentalID(RentalID): 
        return jsonify({"error": "Invalid Rental ID"}), 400

    if not checkRentalStatus(RentalID): 
        return jsonify({"error": "This Rental Transaction has already been closed"}), 400

    session['RentalID'] = RentalID

    return jsonify({
        "Rental Registration": confirmRentalID(RentalID).to_dict(orient='records'),
        "Message": "Please confirm the details"
    }), 200
# dry_run_close_entry

# Primary Validation : Process Input and perform modification if Validation Check passes
def close_entry(RentalID):

    # Primary Validation 
    if not validateRentalID(RentalID) or not checkRentalStatus(RentalID): 
        return jsonify({"error": "Primary Validation Failed"})

    # Generate today's Date as ReturnDate
    ReturnDate = generateDate()
    ReturnDate = ReturnDate.strftime('%Y-%m-%d') # Format it 

    # Read CSV file into DataFrame 
    df = pd.read_csv(CSV_FILE)

    # Update dependent columns on files VideoGames.csv and Members.csv 
    VideoGameID = df.loc[df.iloc[:, 0] == RentalID].iloc[0, 1] # Extract VideoGameID
    MemberID = df.loc[df.iloc[:, 0] == RentalID].iloc[0, 2] # Extract MemberID

    returnGame(VideoGameID) 
    decRentals(MemberID)

    # Modify Return Date and Status 
    df.loc[df['RentalID'] == RentalID, ['ReturnDate', 'Status']] = [ReturnDate, 'Inactive']

    # Save updated DataFrame back to CSV file 
    df.to_csv(CSV_FILE, index=False)

    # Return the updated DataFrame as JSON 
    return jsonify(df.to_dict(orient='records')), 200
# close_entry

@closerental_bp.route('/close_rental', methods=['POST'])
def close_rental_route(): 

    data = request.json # Get json data from POST body 

    # Dry Run: Initial Validation and confirmation 
    if 'Confirm' not in data: 
        return dry_run_close_entry(data.get('RentalID'))

    # Confirm : Primary validation and proceed with closing entry if check passes 
    if data.get('Confirm').lower() == 'confirmed': 
        RentalID = session.get('RentalID')
        return close_entry(RentalID)
    else: 
        return jsonify({"message": "Operation cancelled"}), 200
# close_rental_route
