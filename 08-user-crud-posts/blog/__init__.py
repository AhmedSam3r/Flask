from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Python39/flaskCodes/05-package-structure/blog/site.db'
app.config['SECRET_KEY'] = '2ee1ab3b023f02962acf192762d3fd0c' #Go to Cmd write Python Enter, Write import secrets, Write secrets.token_hex(16)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from blog import routes
