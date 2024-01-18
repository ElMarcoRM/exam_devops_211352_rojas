from flask import Flask, render_template, session, request, redirect, url_for, flash
from sqlalchemy import MetaData, create_engine, text
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from os import getenv, environ
from config import CONFIG

app = Flask(__name__)

application = app
load_dotenv('.env' if getenv('ENV') == 'production' else '../.env')
app.config.from_object(CONFIG)

# БД
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
# print(environ)
print(app.config)

# Создание базы данных при первичном запуске
with create_engine(app.config['MYSQL_ENGINE_URI']).connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {app.config['DB_NAME']}"))

migrate = Migrate(app, db)

from models import *


@app.route('/')
def index():
    test1 = Tests(test='test1')
    db.session.add(test1)
    db.session.commit()
    return render_template('index.html')