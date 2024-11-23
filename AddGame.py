import pandas as pd
import flask_cors import CORS
from fetchDetails import get_g, write_games
from validateEntries import generateVideoGameID
from flask import request, jsonify, Blueprint, session

# This file allows the user to add new entries to the Video Games Table 

# Blueprint
addgame_bp = Blueprint('AddGame', __name__)
CORS(addgame_bp)
addgame_bp.secret_key = 'supersecretkey' # Session Management

# Global Variables 
df = get_g() # Video Games DataFrame 

@addgame_bp.route('/add_game', methods=['POST'])
def add_game_route(): 

    # Update global DataFrame
    global df 
    df = get_g()

    data = request.json # Get json data from POST body

# add_game_route

