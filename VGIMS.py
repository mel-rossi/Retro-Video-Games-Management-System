from flask import Flask, render_template, send_from_directory
import webbrowser
import subprocess
import os
import signal

# this program serves as the main entry point for the webapp
# when ran, opens main page and runs all the flask apps on startup
# also makes the url pretty instead of '.html'

app = Flask(__name__, template_folder='front-end/html')

@app.route('/css/<path:filename>') # needed to handle multiple static folders 
def serve_css(filename):
    return send_from_directory('front-end/css', filename)

@app.route('/js/<path:filename>') # needed to handle multiple static folders 
def serve_js(filename):
    return send_from_directory('front-end/js', filename)

def run_services(): # runs flask apps as subprocesses
    subprocess.Popen(['python', 'SearchGame.py']) 
    subprocess.Popen(['python', 'MemberRental.py'])
    subprocess.Popen(['python', 'GameRental.py'])
    # add more in the future

@app.route('/shutdown', methods=['POST']) # should be called when javascript detects the tab/app has been closed
def shutdown(): # shuts down flask apps
    os.kill(os.getpid(), signal.SIGTERM)
    return 'Shutting down app'

@app.route('/') # opens main page on startup
def main_page():
    return render_template('mainPage.html')

@app.route('/games') # opens available games page
def search_games_page():
    return render_template('availableGames.html')

if __name__ == '__main__':
    run_services()
    webbrowser.open('http://127.0.0.1:5000/') # opens browser
    app.run(port=5000) # runs on port 5000, other flask apps should run on different ports
