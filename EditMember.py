import os 
import pandas as pd 
from flask_cors import CORS
from validateEntries import validateMemberID 
from flask import request, jsonify, Blueprint, session 

# This file allows the use to edit Member Registrations 

editmember_bp = Blueprint('EditMember', __name__)
CORS(editmember_bp) 
editmember_bp.secret_key = 'supersecretkey' # Session Management 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
CSV_FILE = os.path.join(INVENTORY_DIR, 'Members.csv') 

# Dry Run : Initial Input Validation
def dry_run_request_member(MemberID): 

    # Validate MemberID 
    if not validateMemberID(MemberID): 
        return jsonify({"error": "Invalid Rental ID"}), 400

    session['MemberID'] = MemberID

    return jsonify({
        "Member Details Requested": confirmMemberID(MemberID)
        "Message": "Please confirm the request"
    }), 200
# dry_run_edit_member

@editrental_bp.route('/edit_member', methods=['POST'])
def edit_member_route(): 
    
    data = request.json # Get json data from POST body 

    # Dry Run Request : Initial Validation for Member Request and confirmation
    if 'Confirm' not in data: 
        return dry_run_request_member(data.get('MemberID')) 

    # Dry Run : Initial Validation and confirmation

# edit_member_route
