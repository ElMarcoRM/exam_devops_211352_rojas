from os import getenv

class CONFIG():
    ENV = getenv('ENV')
    SECRET_KEY = getenv('SECRET_KEY')
    DB_NAME = getenv('MYSQL_DATABASE')
    MYSQL_HOST = getenv("MYSQL_HOST" if ENV == "production" else "MYSQL_DEV_HOST")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{getenv("MYSQL_USER")}:{getenv("MYSQL_PASSWORD")}@{MYSQL_HOST}:3306/{DB_NAME}'
    MYSQL_ENGINE_URI = f'mysql+mysqlconnector://{getenv("MYSQL_USER")}:{getenv("MYSQL_PASSWORD")}@{MYSQL_HOST}:3306'