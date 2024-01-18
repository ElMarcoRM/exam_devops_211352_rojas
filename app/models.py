import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app
from app import db
from sqlalchemy.sql import func

class Tests(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.String(100))



def create_models(app):
    with app.app_context():
        db.create_all()