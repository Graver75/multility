import os
from dotenv import load_dotenv


from app.db import DB

load_dotenv()

MYSQL_LOGIN = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')


db = DB(MYSQL_LOGIN, MYSQL_PASSWORD, MYSQL_HOST, 'multility')
Base = db.Base

from . import User

def create_tables():
    db.create_tables()
