import pandas as pd
from flask_cors import CORS
from validateEntries import checkTitleEx
from fetchDetails import get_g, write_games
from validateEntries import generateLastRank
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

    session['Title'] = Title
    session['Publisher'] = Publisher
    session['Year'] = Year
    session['Inventory'] = Inventory 
    session['Genre'] = Genre

    return jsonify({
        "Title Entered": Title, 
        "Publisher Entered": Publisher, 
        "Year Entered": Year, 
        "Inventory Entered": Inventory, 
        "Genre(s) Entered": Genre,
        "message": "Please confirm the details"
    }), 200
# dry_run_add_game

def fullValidation(Title, Publisher, Year, Inventory, Genre): 
    if not checkTitleEx(Title) and \
       validatePublisherFormat(Publisher) and \
       validateYearFormat(Year) and \
       validateInventoryFormat(Inventory) and \
       validateGenreFormat(Genre):
           return True 

    return False
# fullValidation

# Primary Validation : Process Input and perform modification if appropriate 
def add_game(Title, Publisher, Year, Inventory, Genre):

    global df 

    # Primary Validation 
    if not fullValidation(Title, Publisher, Year, Inventory, Genre): 
        return jsonify({"error": "Session Transaction Glitch Detected"})

    # Generate the valid next VideoGameID for the Game being added
    VideoGameID = generateVideoGameID()

    # Set Availability to Available 
    Availability = 'Available'

    # Generate New Last Rank 
    Rank = generateLastRank()

    # Make a new row (registration) 
    row = { 'VideoGameID': VideoGameID, 
            'Title': Title, 
            'Publisher': Publisher, 
            'Year': Year, 
            'Availability': Availability, 
            'Inventory': Inventory, 
            'Genre': Genre, 
            'Rank': Rank
    }

    row = pd.DataFrame(row, index=[0]) # Convert to DataFrame 

    df = pd.concat([df, row], ignore_index=True) # Update DataFrame

    # Save updated DataFrame back to CSV file 
    write_games(df)

    # Return the updated row as JSON
    return jsonify({"Registration Added": row.to_dict(orient='records')}), 200

# add_game

@addgame_bp.route('/add_game', methods=['POST'])
def add_game_route(): 

    # Update global DataFrame
    global df 
    df = get_g()

    data = request.json # Get json data from POST body

    # Dry Run: Initial validation and confirmation
    if 'Confirm' not in data: 
        return dry_run_add_game(data.get('Title'), 
                                data.get('Publisher'), 
                                data.get('Year'), 
                                data.get('Inventory'), 
                                data.get('Genre'))

    # Confirm: Primary validation and (if valid) add game
    if data.get('Confirm').lower() == 'confirmed': 
        Title = session.get('Title')
        Publisher = session.get('Publisher')
        Year = session.get('Year')
        Inventory = session.get('Inventory')
        Genre = session.get('Genre')
        return add_game(Title, Publisher, Year, Inventory, Genre)

    else: 
        return jsonify({"message": "Operation cancelled"}), 200
# add_game_route

