from os import environ as env

SECRET_KEY = env.get("SECRET_KEY", "really TOP secret here!!")
SQLALCHEMY_DATABASE_URI = env.get("DATABASE_URI", "sqlite:///omnichat.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True