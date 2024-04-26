from flask import Flask
from flask_login import LoginManager, login_manager
from admin import admin
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'db')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_dir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


def read_input(input):
    with open(input, 'r') as f:
        return f.readline().rstrip()


secret_key = os.getenv('SECRET_KEY')
app.secret_key = secret_key
app.config['SECRET_KEY'] = secret_key

from models import Project, User

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.init_app(app)

from views import ProjectView

admin.add_view(ProjectView(Project))

if __name__ == "__main__":
    app.run(debug=False)
