import os 
import pandas as pd 
from flask_cors impport CORS
from flask import request, jsonify, Blueprint, session 

# This file allows the use to edit Member Registrations 

editmember_bp = Blueprint('EditMember', __name__)
CORS(editmember_bp) 
editmember_bp.secret_key = 'supersecretkey' # Session Management 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory') 
CSV_FILE = os.path.join(INVENTORY_DIR, 'Members.csv') 

# Dry Run : Initial Input Validation 
