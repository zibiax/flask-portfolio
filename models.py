from app import db
from flask_login import UserMixin

class Project(db.Document):
    name = db.StringField()
    description = db.StringField()
    production_url = db.StringField()
    image = db.FileField()

    def __str__(self):
        return self.name

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
