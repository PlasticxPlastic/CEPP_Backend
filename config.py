import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://pontakorn:Eukaryotic1549_@localhost/CEPP_MAFIA_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False