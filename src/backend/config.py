from os import environ, path
from dotenv import load_dotenv

load_dotenv()

# Grabs the folder where the script runs.
basedir = path.abspath(path.dirname(__file__))

# Enable debug mode.
DEBUG = False

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = environ.get('SECRET_KEY')

# Connect to the database
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', "sqlite://")
