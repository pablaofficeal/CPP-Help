from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager
import logging
from logging import basicConfig, DEBUG
from logging.handlers import RotatingFileHandler
from datetime import datetime

basicConfig(level=DEBUG, filename='app.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')
file_handler = RotatingFileHandler('app.log', 'a', 1000000, 1)
file_handler.setLevel(DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
basicConfig(handlers=[file_handler])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

db = SQLAlchemy(app)
Session(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'       

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)
    is_published = db.Column(db.Boolean, default=False)  
    
with app.app_context():
    db.create_all()    

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=False)