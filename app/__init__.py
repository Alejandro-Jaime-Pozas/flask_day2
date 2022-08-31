from flask import Flask # Flask class from the flask package
from config import Config # this config refers to class in file config.py, refers to database stuff
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy package allows python > sql tables/translation/communication?
from flask_migrate import Migrate # migrate allows for new data to populate in database?
from flask_login import LoginManager


app = Flask(__name__) # calls Flask class in flask package with input __name__
app.config.from_object(Config)
# app.config['SECRET_KEY'] = 'you-will-never-guess' # creates a secret key into app into config which is
# the subclass of a dict and acts the same as a dict
# this secret key is a CSRF token that needs to be validated before being submitted


# create an instance of SQLAlchemy (the ORM) w the Flask Application
db = SQLAlchemy(app)
# create an instance of Migrate which will be our migration engine and pass in the app and SQLAlchemy instance
migrate = Migrate(app, db)
# create an instance of the LoginManager to handle authentication for users
login = LoginManager(app)
login.login_view = 'login' # tells the login manager which endpoint to redirect if someone is not logged in
login.login_message_category = 'danger'

### ADDED FOR API FN
from app.blueprints.api import api
app.register_blueprint(api)

from . import routes, models # you need to include this AFTER flask instance to avoid infinite loop...the . refers to the current folder; 
