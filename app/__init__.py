from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '86bd6b2b94c7e4714ea903f6e603673b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lwuqqwelpqxirt:85b1c87d869cd31c514fda79ef79e061c7008b9614875bf10cd63412f380d183@ec2-34-193-117-204.compute-1.amazonaws.com:5432/d4knpp6d2pn40f'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes