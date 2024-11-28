import pandas as pd 
from flask_cors import CORS
from fetchDetails import gameYear
from fetchDetails import gameGenre
from fetchDetails import gameTitle
from fetchDetails import gamePublisher
from fetchDetails import gameInventory
from validateEntries import checkTitleEx
from fetchDetails import get_g, write_games
from validateEntries import validateNumInsert
from validateEntries import validateInsertion
from validateEntries import confirmVideoGameID
from validateEntries import validateVideoGameID
from validateEntries import validateGenreFormat
from validateEntries import validateInventoryFormat
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

def changeRequest(Title, Publisher, Year, Inventory, Genre): 
    if Title is None and \
       Publisher is None and \
       Year is None and \
       Inventory is None and \
       Genre is None: 
           return False 

    return True 
# changeRequest

# Dry Run : Initial Input Validation After Successful Request 
def dry_run_edit_game(VideoGameID, Title, Publisher, Year, Inventory, Genre, mode):

    no = '[No Changes]'

    # Request Validation 
    if not validateVideoGameID(VideoGameID): 
        return jsonify({"error": "Session Transaction Glitch Detected"}), 400

    # Change Validation
    if not changeRequest(Title, Publisher, Year, Inventory, Genre): 
        return jsonify({"error": "No Changes are Being Requested"}), 400

    # Insert Editing Mode
    if mode is not None and mode.lower() == 'insert':

        # Insert to Title
        if Title is not None: # Concat Title 
            Title = gameTitle(VideoGameID) + Title 

        # Insert to Publisher
        if Publisher is not None: # Concat Publisher
            Publisher = gamePublisher(VideoGameID) + Publisher 

        # Insert to Year
        if Year is not None and validateInsertion(Year) and \
           validateNumInsert(Year[1:]): 
               if Year.startswith('+'): # Increment(+) Year #
                   Year = int(gameYear(VideoGameID)) + \
                          int(Year[1:])

               else: # Decrement(-) Year #
                   Year = int(gameYear(VideoGameID)) - \
                          int(Year[1:])

        # Insert to Inventory
        if Inventory is not None and validateInsertion(Inventory) and \
           validateInventoryFormat(Inventory[1:]):
               if Inventory.startswith('+'): # Increment(+) Inventory #
                   Inventory = int(gameInventory(VideoGameID)) + \
                               int(Inventory[1:])

               else: # Decrement(-) Inventory #
                   if int(Inventory[1:]) >= gameInventory(VideoGameID): 
                       Inventory = 0

                   else: 
                       Inventory = int(gameInventory(VideoGameID)) - \
                                   int(Inventory[1:])

        # Insert to Genre
        if Genre is not None and validateInsertion(Genre) and \
           validateGenreFormat(Genre[1:]):
               if Genre.startswith('+'): # Add Genre(s)
                   Genre = gameGenre(VideoGameID) + "/" + Genre[1:]

               else: # Delete Genre(s)
                   if ('/' + Genre[1:]) in gameGenre(VideoGameID): 
                       Genre = gameGenre(VideoGameID).\
                               replace(('/' + Genre[1:]), "")

                   elif (Genre[1:] + '/') in gameGenre(VideoGameID): 
                       Genre = gameGenre(VideoGameID).\
                               replace((Genre[1:] + '/'), "")

                   else: 
                       return jsonify({"error": "Genre Requested To Be \
                               Removed Doesn't Exist or is the only Genre \
                               this Video Game Is Filed Under"}), 400

    # Change Request Validation 

    # Validate Title 
    if Title is not None:
        if checkTitleEx(Title): 
            return jsonify({"error": "Invalid Requested Changes for Title: \
                            Title Already Registered in System"}), 400

    # Validate Publisher
    if Publisher is not None:
        if not validatePublisherFormat(Publisher): 
            return jsonify({"error": "Invalid Requested Changes \
                    for Publisher"}), 400

    # Validate Year
    if Year is not None: 
        if not validateYearFormat(str(Year)): 
            return jsonify({"error": "Invalid Requested Changes for \
                    Year"}), 400

    # Validate Inventory
    if Inventory is not None:
        if not validateInventoryFormat(str(Inventory)):
            return jsonify({"error": "Invalid Requested Changes for \
                    Inventory"}), 400

    # Validate Genre 
    if Genre is not None:
        if not validateGenreFormat(Genre): 
            return jsonify({"error": "Invalid Requested Changes for \
                    Genre"}), 400

    session['VideoGameID'] = VideoGameID
    session['Title'] = Title 
    session['Publisher'] = Publisher 
    session['Year'] = Year
    session['Inventory'] = Inventory 
    session['Genre'] = Genre 

    return jsonify({ 
        "Video Game Registration Being Edited": \
                confirmVideoGameID(VideoGameID).to_dict(orient='records'),
        "Editing Mode": "Insert (Increment / Decrement / Concatenate)"
                if mode is not None and mode.lower == 'insert' \
                else "Overtype (Overwriting)",
        "Title Requested Changes": Title \
                if Title is not None else no, 
        "Publisher Requested Changes": Publisher \
                if Publisher is not None else no,
        "Year Requested Changes": Year \
                if Year is not None else no, 
        "Inventory Requested Changes": Inventory \
                if Inventory is not None else no, 
        "Genre Requested Changes": Genre \
                if Genre is not None else no
    }), 200
# dry_run_edit_game

def fullValidation(VideoGameID, Title, Publisher, Year, Inventory, Genre): 

    if validateVideoGameID(VideoGameID) and \
       changeRequest(Title, Publisher, Year, Inventory, Genre) and \
       (Title is None or not checkTitleEx(Title)) and \
       (Publisher is None or validatePublisherFormat(Publisher)) and \
       (Year is None or validateYearFormat(str(Year))) and \
       (Inventory is None or validateInventoryFormat(str(Inventory))) and \
       (Genre is None or validateGenreFormat(Genre)): 
           return True 

    return False
# fullValidation

def edit_game(VideoGameID, Title, Publisher, Year, Inventory, Genre): 

    global df 

    # Primary Validation 
    if not fullValidation(VideoGameID, Title, Publisher, Year, Inventory, Genre): 
        return jsonify({"error": "Session Transaction Glitch Detected"})

    # Modify Title 
    if Title is not None: 
        df.loc[df['VideoGameID'] == VideoGameID, 'Title'] = Title 

    # Modify Publisher 
    if Publisher is not None: 
        df.loc[df['VideoGameID'] == VideoGameID, 'Publisher'] = Publisher

    # Modify Year 
    if Year is not None: 
        df.loc[df['VideoGameID'] == VideoGameID, 'Year'] = Year

    # Modify Inventory 
    if Inventory is not None: 
        df.loc[df['VideoGameID'] == VideoGameID, 'Inventory'] = Inventory

    # Modify Genre(s) 
    if Genre is not None: 
        df.loc[df['VideoGameID'] == VideoGameID, 'Genre'] = Genre

    # Save updated DataFrame back to CSV file 
    write_games(df) 

    row = df[df['VideoGameID'] == VideoGameID] # Updated row

    # Return the updated row 
    return jsonify(row.to_dict(orient='records')), 200
# edit_game

@editgame_bp.route('/edit_game', methods=['POST'])
def edit_game_route(): 

    # Update global DataFrame 
    global df 
    df = get_g() 

    data = request.json # Get json data from POST body 

    # Dry Run Request : Initial Validation for Video Game Request and confirmation
    if 'Request' not in data and 'Confirm' not in data: 
        return dry_run_request_game(data.get('VideoGameID'))

    # Dry Run : Initial Validation and confirmation
    if 'Confirm' not in data: 
        if data.get('Request').lower() == 'verified': 
            VideoGameID = session.get('VideoGameID')
            return dry_run_edit_game(VideoGameID, 
                                     data.get('Title'), 
                                     data.get('Publisher'), 
                                     data.get('Year'), 
                                     data.get('Inventory'), 
                                     data.get('Genre'),
                                     data.get('mode'))
        else: 
            return jsonify({"message": "Request cancelled"}), 200

    # Confirm : Primary Validation and proceed with editing entry if appropriate 
    if data.get('Confirm').lower() == 'confirmed': 
        VideoGameID = session.get('VideoGameID')
        Title = session.get('Title') 
        Publisher = session.get('Publisher') 
        Year = session.get('Year')
        Inventory = session.get('Inventory') 
        Genre = session.get('Genre') 
        return edit_game(VideoGameID, Title, Publisher, Year, Inventory, Genre) 
    else: 
        return jsonify({"message": "Operation cancelled"}), 200
# edit_game_route
