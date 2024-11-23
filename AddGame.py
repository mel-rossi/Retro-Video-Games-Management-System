import pandas as pd
import flask_cors import CORS
from validateEntries import checkTitleEx
from fetchDetails import get_g, write_games
from validateEntries import validateYearFormat
from validateEntries import generateVideoGameID
from validateEntries import validateGenreFormat
from validateEntries import validatePublisherFormat
from validateEntries import validateInventoryFormat
from flask import request, jsonify, Blueprint, session

# This file allows the user to add new entries to the Video Games Table 

# Blueprint
addgame_bp = Blueprint('AddGame', __name__)
CORS(addgame_bp)
addgame_bp.secret_key = 'supersecretkey' # Session Management

# Global Variables 
df = get_g() # Video Games DataFrame

# Dry Run : Initial Input Validation 
def dry_run_add_game(Title, Publisher, Year, Inventory, Genre):

    # Validate Title 
    if Title is None: 
        return jsonify({"error": "Title Missing"}), 400

    if checkTitleEx(Title): 
        return jsonify({"error": "Title Already Registered \
                        in System"}), 400

    # Validate Publisher 
    if Publisher is None: 
        return jsonify({"error": "Publisher Missing"}), 400

    if not validatePublisherFormat(Publisher): 
        return jsonify({"error": "Invalid Publisher Format"}), 400

    # Validate Year
    if Year is None: 
        return jsonify({"error": "Year Missing"}), 400

    if not validateYearFormat(Year): 
        return jsonify({"error": "Invalid Year Format"}), 400

    # Validate Inventory 
    if Inventory is None: 
        return jsonify({"error": "Inventory Missing"}), 400

    if not validateInventoryFormat(Inventory):
        return jsonify({"error": "Invalid Inventory Format"}), 400

    # Validate Genre
    if Genre is None: 
        return jsonify({"error": "Genre(s) Missing"}), 400
    
    if not validateGenreFormat(Genre): 
        return jsonify({"error": "Invalid Genre(s) Format"}), 400

# dry_run_add_game

@addgame_bp.route('/add_game', methods=['POST'])
def add_game_route(): 

    # Update global DataFrame
    global df 
    df = get_g()

    data = request.json # Get json data from POST body

    # Dry Run: Initial validation and confirmation

# add_game_route

