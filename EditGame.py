import pandas as pd 
from flask_cors import CORS
from fetchDetails import get_g, write_games
from validateEntries import confirmVideoGameID
from validateEntries import validateVideoGameID
from validateEntries import validateGenreFormat
from flask import request, jsonify, Blueprint, session

# This file allows the user to edit Video Game Registrations 

# Blueprint 
editgame_bp = Blueprint('EditGame', __name__) 
CORS(editgame_bp)
editgame_bp.secret_key = 'supersecretkey' # Session Management 

# Global Variables 
df = get_g() # Video Games DataFrame 

# Dry Run Request : Initial Input Validation for Requested Registrations 
def dry_run_request_game(VideoGameID): 

    # Validate VideoGameID 
    if not validateVideoGameID(VideoGameID): 
        return jsonify({"error": "Invalid Video Game ID"}), 400

    session['VideoGameID'] = VideoGameID 

    return jsonify({ 
        "Video Game Details Requested": \
                confirmVideoGameID(VideoGameID).to_dict(orient='records'),
        "Message": "Please confirm the request"
    }), 200
# dry_run_request_game

@editgame_bp.route('/edit_game', methods=['POST'])
def edit_game_route(): 

    # Update global DataFrame 
    global df 
    df = get_g() 

    data = request.json # Get json data from POST body 

    # Dry Run Request : Initial Validation for Video Game Request and confirmation
    if 'Request' not in data and 'Confirm' not in data: 
        return dry_run_request_game(data.get('VideoGameID'))
    
# edit_game_route
