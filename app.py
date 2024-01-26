from flask import Flask
from flask_login import LoginManager, login_manager
from admin import admin
import os

app = Flask(__name__)

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'db')

app.config['MONGODB_SETTINGS'] = {
        'db': 'Project',
        'host': f'mongodb://localhost:27017/Project'
        }


def read_input(input):
    with open(input, 'r') as f:
        return f.readline().rstrip()

secret_key = read_input('secret_key.txt')
app.secret_key = secret_key
app.config['SECRET_KEY'] = secret_key

from models import db, Project, User


db.init_app(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

login_manager.init_app(app)

from views import ProjectView

admin.add_view(ProjectView(Project))

if __name__ == "__main__":
    app.run(debug=True)
