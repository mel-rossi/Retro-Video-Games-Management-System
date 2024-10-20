import os
import signal
import webbrowser
from Rank import rank_bp
from SearchGame import searchgame_bp
from GameRental import gamerental_bp
from RentalStat import rentalstat_bp
from MemberRental import memberrental_bp
from flask import Flask, render_template, send_from_directory

# This program serves as the main entry point for the Web Application
# When ran, opens main page and runs all the flask apps on startup
# Also makes the url pretty instead of '.html'

app = Flask(__name__, template_folder='front-end/html')

app.register_blueprint(searchgame_bp, url_prefix='')
app.register_blueprint(gamerental_bp, url_prefix='')
app.register_blueprint(memberrental_bp, url_prefix='')
app.register_blueprint(rentalstat_bp, url_prefix='') 
app.register_blueprint(rank_bp, url_prefix='')

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

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5500/VGIMS') # opens browser
    app.run(port=5500) # runs on port 5500
