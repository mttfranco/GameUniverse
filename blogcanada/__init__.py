from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '2ed72a9002655244278c8bac86ace36a'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projetoblog.db'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from blogcanada import routes
