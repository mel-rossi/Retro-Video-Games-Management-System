import os
import signal
import webbrowser
import bcrypt
from Rank import rank_bp
from Rank import sortingMethod
from AddMember import addmember_bp
from EditMember import editmember_bp
from OpenRental import openrental_bp
from SearchGame import searchgame_bp
from GameRental import gamerental_bp
from RentalStat import rentalstat_bp
from CloseRental import closerental_bp
from SearchMember import searchmember_bp
from MemberRental import memberrental_bp
from fetchDetails import read_rentals, read_members, read_games
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, session, g
from flask_session import Session
from datetime import timedelta
from filelock import FileLock, Timeout

# This program serves as the main entry point for the Web Application
# When ran, opens main page and runs all the flask apps on startup
# Also makes the url pretty instead of '.html'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_DIR = os.path.join(BASE_DIR, 'Inventory')
MEMBER_PATH = os.path.join(INVENTORY_DIR, 'Members.csv')
RENTAL_PATH = os.path.join(INVENTORY_DIR, 'Rentals.csv')
VIDEOGAME_PATH = os.path.join(INVENTORY_DIR, 'VideoGames.csv')
SESSIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessions') 
FILE_PATHS = {VIDEOGAME_PATH, RENTAL_PATH, MEMBER_PATH}

app = Flask(__name__, template_folder='front-end/html')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # automatically deletes session after 30 mins
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = SESSIONS
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)
app.secret_key = 'supersecretkey' # Set secret key

app.register_blueprint(searchgame_bp, url_prefix='')
app.register_blueprint(gamerental_bp, url_prefix='')
app.register_blueprint(memberrental_bp, url_prefix='')
app.register_blueprint(rentalstat_bp, url_prefix='') 
app.register_blueprint(rank_bp, url_prefix='')
app.register_blueprint(searchmember_bp, url_prefix='')
app.register_blueprint(openrental_bp, url_prefix='')
app.register_blueprint(closerental_bp, url_prefix='')
app.register_blueprint(addmember_bp, url_prefix='')
app.register_blueprint(editmember_bp, url_prefix='')

def rank_update(): # updates/resorts videogames.csv by rank in ascending order
    ranked = sortingMethod('game','','','') # sort the file by score
    ranked['Rank'] = range(1, len(ranked) + 1) # overwrite existing rank column values
    ranked.sort_values(by='VideoGameID', ascending=True, inplace=True) # sort by videogameid
    ranked.to_csv('Inventory/VideoGames.csv', index=False) # overwrite exiting videogames.csv file
# rank_update

def init_scheduler(): # runs rank_update depending on schedule (currently set to midnight 00:00)
    scheduler = BackgroundScheduler()
    scheduler.add_job(rank_update, 'cron', hour=0, minute=0) # uses 24 hour time format
    scheduler.start()
# init_scheduler

@app.route('/css/<path:filename>') # handle multiple static folders 
def serve_css(filename):
    return send_from_directory('front-end/css', filename)

@app.route('/js/<path:filename>') # handle multiple static folders 
def serve_js(filename):
    return send_from_directory('front-end/js', filename)

@app.route('/shutdown', methods=['POST']) # called when javascript detects the tab/app was closed
def shutdown(): # shuts down flask apps
    os.kill(os.getpid(), signal.SIGTERM)
    return 'Shutting down app'

@app.route('/VGIMS') # opens main page on startup
def main_page():
    return render_template('mainPage.html')

@app.route('/VGIMS/games') # opens available games page
def search_games_page():
    return render_template('availableGames.html')

@app.route('/VGIMS/status') # opens customer status page
def customer_status_page():
    return render_template('customerStatus.html')

 # opens gamestats page, to open a specific id:
 # gamestats?ID=[insert videogame id]
@app.route('/VGIMS/gamestats')
def gamestats_route():
    id = request.args.get('ID')
    return render_template('gameStats.html', videogame_id=id)
# sends videogame_id as a parameter to gamestats_html
# gamestats_route

@app.route('/VGIMS/login') # opens login page
def login_page():
    return render_template('loginPage.html')  # set to open main page temporarily

@app.route('/VGIMS/manage') # opens manage page for editing/adding entries
def manage_page():
    id = request.args.get('ID')
    action = request.args.get('M_State')
    return render_template('manageGames.html', game_id=id, manage_state=action)

@app.route('/authenticator', methods=['POST']) # call route to check password when logging in
def authenticator():
    data = request.json # parameters: {'password': [INSERT PASSWORD]}
    with open('encrypted_keys', 'rb') as f:
        for pw in f:
            if bcrypt.checkpw(data.get('password').encode(), pw.strip()):
                session['logged_in'] = True # creates session if password is correct
                return jsonify({'valid': True, 'redirect_url' : '/VGIMS'})
    return jsonify({'valid' : False})
# authenticator route

# call route to change passwords (admin or employee)
# when logged in admins should only have a button to call this route
@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json 
    # parameters: {'change_type': ['employee' else admin], 'password': [INSERT PASSWORD]}
    pw = bcrypt.hashpw(data.get('password').encode(), bcrypt.gensalt())
    f = open('encrypted_keys', 'rb')
    lines = f.readlines()
    if data.get('change_type') == 'employee':
        lines[1] = pw
    else:
        lines[0] = pw + b'\n'
    f = open('encrypted_keys', 'wb')
    f.writelines(lines)
    f.close()
# change password route

@app.route('/logout', methods=['POST']) # route for manual logout button click
def logout():
    session.pop('logged_in', None)  # clears current session
    return jsonify({'redirect_url' : '/VGIMS/login'})  # sends redirection route as a param
# logout route

@app.before_request # check session expiration before each request is sent
def check_session():
    writing_routes = ['/open_rental', '/close_rental', 
                      '/edit_member', '/add_member']
    excluded_routes = ['authenticator'] # routes not effected
    g.locks = {}
    if request.path in writing_routes:
        for path in FILE_PATHS:
            try:
                lock_path = f'{path}.lock'
                g.locks[path] = FileLock(lock_path, timeout=5)
                g.locks[path].acquire()
            except Timeout:
                return jsonify('Error, another write is occurring.'), 409
    if request.endpoint in excluded_routes:
        return None
    if request.path.startswith('/css') or request.path.startswith('/js'): 
        return None
    if 'logged_in' not in session and request.path != '/VGIMS/login':
        return redirect('/VGIMS/login') # send to login page if expired

@app.after_request # (re) read the CSVs
def refresh_csv(response): 
    read_rentals() 
    read_members() 
    read_games()
    for lock in g.locks.values():
        lock.release() 
    return response

 # check session expiration at specific intervals
 # javascript frontend needs to call this route and handle logic    
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    excluded_routes = ['authenticator'] # routes not effected
    if request.endpoint in excluded_routes:
        return None
    if request.path.startswith('/css') or request.path.startswith('/js'): 
        return None
    if 'logged_in' not in session and request.path != '/VGIMS/login':
        return redirect('/VGIMS/login') # send to login page if expired

if __name__ == '__main__':
    init_scheduler() # updates videogames.csv ranking at midnight 00:00
    webbrowser.open('http://127.0.0.1:5500/VGIMS/login') # opens browser
    app.run(port=5500) # runs on port 5500
