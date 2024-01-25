from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
        'db': 'Project',
        'host': 'localhost'
        }

db = MongoEngine(app)
login_manager = LoginManager(app)

def read_input(input):
    with open(input, 'r') as f:
        return f.readline().rstrip()

secret_key = read_input('secret_key.txt')
app.secret_key = secret_key
app.config['SECRET_KEY'] = secret_key

admin = Admin(app, name='Admin', template_mode='bootstrap4')


if __name__ == "__main__":
    app.run(debug=False)
