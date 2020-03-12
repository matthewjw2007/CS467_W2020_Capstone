# File to save global configuration variables
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # This is used to generate signatures or tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-secret-password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Below is used to signal the application every time a change will be made to the database if set to true
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    # Used for Heroku
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
