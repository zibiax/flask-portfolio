from flask import Flask
from flask_login import LoginManager
from admin import admin
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from models import Project, User
from views import ProjectView

app = Flask(__name__)

app.logger.setLevel(logging.INFO)  # Set log level to INFO

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()  # Output log messages to console
console_handler.setLevel(logging.INFO)    # Set console log level to INFO
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)


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


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


login_manager.init_app(app)


admin.add_view(ProjectView(Project))

if __name__ == "__main__":
    app.run(debug=False)
