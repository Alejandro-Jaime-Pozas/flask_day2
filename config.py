import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # setting up the configuration for the application. pull from environment variables using os.environ.get()
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # get will look for secret key and return that value, and if that returns None, will continue to OR stmt
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') # this checks if no database existing, will return sqlite database directory
    SQLALCHEMY_TRACK_MODIFICATIONS = False