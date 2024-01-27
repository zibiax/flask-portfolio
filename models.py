from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    production_url = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def __repr__(self):
        return f'<Project {self.name}>'
