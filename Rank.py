# This program sorts .CSVs by
import os 
import pandas as pd 
from flask_cors import CORS 
from flask import request, jsonify, Blueprint 

rank_bp = Blueprint('Rank', __name__) 
CORS(rank_bp)

# Load the .csv files 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_FIR, 'Inventory') 
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv') 
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv') 
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv') 

# Read .csv files into DataFrames 
df1 = pd.read_csv(MEMBER_PATH) 
df2 = pd.read_csv(RENTAL_PATH) 
df3 = pd.read_csv(VIDEOGAME_PATH) 

# Functions 
