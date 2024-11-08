import os
import signal
import webbrowser
import bcrypt
from Rank import rank_bp
from Rank import sortingMethod
from OpenRental import openrental_bp
from SearchGame import searchgame_bp
from GameRental import gamerental_bp
from RentalStat import rentalstat_bp
from CloseRental import closerental_bp
from SearchMember import searchmember_bp
from MemberRental import memberrental_bp
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, send_from_directory, jsonify

# This program serves as the main entry point for the Web Application
# When ran, opens main page and runs all the flask apps on startup
# Also makes the url pretty instead of '.html'

app = Flask(__name__, template_folder='front-end/html')
app.secret_key = 'supersecretkey' # Set secret key

app.register_blueprint(searchgame_bp, url_prefix='')
app.register_blueprint(gamerental_bp, url_prefix='')
app.register_blueprint(memberrental_bp, url_prefix='')
app.register_blueprint(rentalstat_bp, url_prefix='') 
app.register_blueprint(rank_bp, url_prefix='')
app.register_blueprint(searchmember_bp, url_prefix='')
app.register_blueprint(openrental_bp, url_prefix='')
app.register_blueprint(closerental_bp, url_prefix='') 

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
def manage_login_page():
    return render_template('mainPage.html')  # set to open main page temporarily

@app.route('/VGIMS/manage') # opens manage page for editing/adding entries
def manage_page():
    return render_template('name of manage file')

@app.route('/authenticator', methods=['POST']) # call route to check password when logging in
def authenticator():
    data = request.json # parameters: {'password': [INSERT PASSWORD]}
    with open('encrypted_keys', 'rb') as f:
        for pw in f:
            if bcrypt.checkpw(data.get('password').encode(), pw.strip()):
                state = 'Success'
            else:
                state = 'Failed'
    f.close()
    return jsonify(state)
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

if __name__ == '__main__':
    init_scheduler() # updates videogames.csv ranking at midnight 00:00
    webbrowser.open('http://127.0.0.1:5500/VGIMS/login') # opens browser
    app.run(port=5500) # runs on port 5500
