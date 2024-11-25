import pandas as pd 
from flask_cors import CORS
from fetchDetails import get_g, write_games
from validateEntries import confirmVideoGameID
from validateEntries import validateVideoGameID
from validateEntries import validateGenreFormat

# This file allows the user to edit Video Game Registrations 

# Blueprint 
editgame_bp = Blueprint('EditGame', __name__) 
CORS(editgame_bp)
editgame_bp.secret_key = 'supersecretkey' # Session Management 

# Global Variables 
df = get_g() # Video Games DataFrame 

# Dry Run Request : Initial Input Validation for Requested Registrations 

@editgame_bp.route('/edit_game', methods=['POST'])
def edit_game_route(): 

    # Update global DataFrame 
    global df 
    df = get_m() 

    data = request.json # Get json data from POST body 

    # Dry Run Request : Initial Validation for Video Game Request and confirmation
    
# edit_game_route
