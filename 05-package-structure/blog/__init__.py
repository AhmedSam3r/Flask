#this file tells python that this is a package
#It initializes and ties everything we need for our app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Python39/flaskCodes/05-package-structure/blog/site.db'
app.config['SECRET_KEY'] = '2ee1ab3b023f02962acf192762d3fd0c' #Go to Cmd write Python Enter, Write import secrets, Write secrets.token_hex(16)
db = SQLAlchemy(app)

from blog import routes
