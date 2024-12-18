import pandas as pd 
from flask_cors import CORS
from validateEntries import confirmMemberID
from validateEntries import validateMemberID
from fetchDetails import get_m, write_members
from validateEntries import validateNameFormat
from validateEntries import validateEmailFormat
from validateEntries import validatePhoneFormat 
from flask import request, jsonify, Blueprint, session 

# This file allows the use to edit Member Registrations 

# Blue Print 
editmember_bp = Blueprint('EditMember', __name__)
CORS(editmember_bp) 
editmember_bp.secret_key = 'supersecretkey' # Session Management 

# Global Variables 
df = get_m() # Members DataFrame

# Dry Run Request : Initial Input Validation for Requested Registration
def dry_run_request_member(MemberID): 

    # Validate MemberID 
    if not validateMemberID(MemberID): 
        return jsonify({"error": "Invalid Member ID"}), 400

    session['MemberID'] = MemberID

    return jsonify({
        "Member Details Requested": \
                confirmMemberID(MemberID).to_dict(orient='records'),
        "Message": "Please confirm the request"
    }), 200
# dry_run_edit_member

# Check if at least one change request is being made
def changeRequest(FirstName, LastName, PhoneNumber, Email):

    if FirstName is None and \
       LastName is None and \
       PhoneNumber is None and \
       Email is None: 
           return False

    return True 
# changeRequest

# Dry Run : Initial Input Validation After Sucessful Request
def dry_run_edit_member(MemberID, FirstName, LastName, PhoneNumber, Email): 

    no = '[No Changes]' 

    # Request Validation 
    if not validateMemberID(MemberID): 
        return jsonify({"error": "Session Transaction Glitch Detected"}), 400
  
    # Change Validation 
    if not changeRequest(FirstName, LastName, PhoneNumber, Email): 
        return jsonify({"error": "No Changes are Being Requested"}), 400 
    
    # Validate FirstName 
    if FirstName is not None: 
        if not validateNameFormat(FirstName):
            return jsonify({"error": "Invalid Format for First Name Given"}), \
                   400

    # Validate LastName 
    if LastName is not None:
        if not validateNameFormat(LastName): 
            return jsonify({"error": "Invalid Format for Last Name Given"}), \
                   400

    # Validate PhoneNumber
    if PhoneNumber is not None:
        if not validatePhoneFormat(PhoneNumber): 
            return jsonify({"error": "Invalid Format for Phone Number Given"}),\
                   400

    # Validate Email 
    if Email is not None: 
        if not validateEmailFormat(Email): 
            return jsonify({"error": "Invalid Format for Email Given"}), 400

    session['MemberID'] = MemberID
    session['FirstName'] = FirstName
    session['LastName'] = LastName
    session['PhoneNumber'] = PhoneNumber 
    session['Email'] = Email 

    return jsonify({
        "Member Registration Being Edited": \
                confirmMemberID(MemberID).to_dict(orient='records'), 
        "First Name Requested Changes": FirstName \
                if FirstName is not None else no,
        "Last Name Requested Changes": LastName \
                if LastName is not None else no, 
        "Phone Number Requested Changes": PhoneNumber \
                if PhoneNumber is not None else no, 
        "Email Requested Changes": Email \
                if Email is not None else no,
        "Message": "Please confirm the details"
    }), 200

# dry_run_edit_member

def fullValidation(MemberID, FirstName, LastName, PhoneNumber, Email): 

    if validateMemberID(MemberID) and \
       changeRequest(FirstName, LastName, PhoneNumber, Email) and \
       (FirstName is None or validateNameFormat(FirstName)) and \
       (LastName is None or validateNameFormat(LastName)) and \
       (PhoneNumber is None or validatePhoneFormat(PhoneNumber)) and \
       (Email is None or validateEmailFormat(Email)): 
           return True

    return False
# fullValidation 

# Primary Validation : Process Input and perform modification if Validation Check passes
def edit_member(MemberID, FirstName, LastName, PhoneNumber, Email): 

    global df

    # Primary Validation 
    if not fullValidation(MemberID, FirstName, LastName, PhoneNumber, Email): 
        return jsonify({"error": "Session Transaction Glitch Detected"})

    # Modify First Name 
    if FirstName is not None:
        df.loc[df['MemberID'] == MemberID, 'FirstName'] = FirstName

    # Modify Last Name 
    if LastName is not None: 
        df.loc[df['MemberID'] == MemberID, 'LastName'] = LastName

    # Modify Phone Number 
    if PhoneNumber is not None: 
        df.loc[df['MemberID'] == MemberID, 'PhoneNumber'] = PhoneNumber 

    # Modify Email 
    if Email is not None: 
        df.loc[df['MemberID'] == MemberID, 'Email'] = Email

    # Save updated DataFrame back to CSV file 
    write_members(df)

    row = df[df['MemberID'] == MemberID]

    # Return the updated row as JSON 
    return jsonify(row.to_dict(orient='records')), 200
# edit_member 

@editmember_bp.route('/edit_member', methods=['POST'])
def edit_member_route():

    # Update global DataFrame
    global df
    df = get_m()
    
    data = request.json # Get json data from POST body 

    # Dry Run Request : Initial Validation for Member Request and confirmation
    if 'Request' not in data and 'Confirm' not in data: 
        return dry_run_request_member(data.get('MemberID')) 

    # Dry Run : Initial Validation and confirmation
    if 'Confirm' not in data: 
        if data.get('Request').lower() == 'verified':
            MemberID = session.get('MemberID') 
            return dry_run_edit_member(MemberID, 
                                       data.get('FirstName'), 
                                       data.get('LastName'), 
                                       data.get('PhoneNumber'), 
                                       data.get('Email'))
        else:  
            return jsonify({"message": "Request cancelled"}), 200

    # Confirm: Primary validation and prooceed with editing entry if appropriate
    if data.get('Confirm').lower() == 'confirmed':
        MemberID = session.get('MemberID') 
        FirstName = session.get('FirstName') 
        LastName = session.get('LastName') 
        PhoneNumber = session.get('PhoneNumber') 
        Email = session.get('Email') 
        return edit_member(MemberID, FirstName, LastName, PhoneNumber, Email)

    else: 
        return jsonify({"message": "Operation cancelled"}), 200

# edit_member_route
