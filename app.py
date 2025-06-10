from flask import Flask, render_template
from flask_session import Session
import logging
from logging import basicConfig, DEBUG
from logging.handlers import RotatingFileHandler
from models import db, User, Post
from config import Config

basicConfig(level=DEBUG, filename='app.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')
file_handler = RotatingFileHandler('app.log', 'a', 1000000, 1)
file_handler.setLevel(DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
basicConfig(handlers=[file_handler])

app = Flask(__name__)
app.config.from_object(Config)

Session(app) 
db.init_app(app)

with app.app_context():
    db.create_all()    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6457, debug=False)