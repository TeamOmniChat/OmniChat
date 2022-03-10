from os import environ as env

SECRET_KEY = env.get("SECRET_KEY") or 'dev'
SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URI") or 'sqlite:///omnichat.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True