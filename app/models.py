import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app
from app import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Tests(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.String(100))

class Workers(db.Model, UserMixin):
    __tablename__ = 'worker'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def count_not_fired():
    return Workers.query.filter(Workers.status == "Работает").count()


class Events(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(10000), nullable=False)

def get_event_year(year):
    return Events.query.filter(Events.year == year).all()


def create_models(app):
    with app.app_context():
        db.create_all()