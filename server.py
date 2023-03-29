# Channel 4 Test App
# Flask server

# Imports
from flask import Flask, render_template

# Declarations
app = Flask(__name__)

# Functions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

# Main

if __name__ == '__main__':
    app.run()