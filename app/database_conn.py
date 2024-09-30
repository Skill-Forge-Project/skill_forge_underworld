import os
import urllib.parse
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# Define the connection parameters as variables
USERNAME = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
ENCODED_PASSWORD = urllib.parse.quote_plus(PASSWORD)
DB_NAME = os.getenv('DB_NAME')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
SQL_URI = f'postgresql://{USERNAME}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

# PostgreSQL connection Init
db = SQLAlchemy()
