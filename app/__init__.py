from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '86bd6b2b94c7e4714ea903f6e603673b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://evuujddmoyucvl:c435005bca38e036db86597a2a6d284253442c31e4aad565ec75d42910357ab8@ec2-34-200-72-77.compute-1.amazonaws.com:5432/dcfmff6debn1u'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import routes