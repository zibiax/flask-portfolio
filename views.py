from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin.form.upload import ImageUploadField
from flask_login import current_user, login_required, login_user, logout_user
from flask import redirect, render_template, abort, session, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Project
from app import app, db
from admin import admin
from flask_admin import Admin
from forms import RegistrationForm
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

migrate = Migrate(app, db)


app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Folder to store uploaded files

# Function to handle file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_project = Project(name=request.form['name'],
                              description=request.form['description'],
                              image_filename=filename)
        db.session.add(new_project)
        db.session.commit()

        return 'File uploaded successfully'

    return 'Invalid file'


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class ProjectView(ModelView):
    column_list = ('name', 'description', 'production_url', 'image')
    create_modal = True
    edit_modal = True
    column_exclude_list = ['created_at']
    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'

    form_extra_fields = {
        'image': ImageUploadField('Image',
                                  base_path=lambda: os.path.join(os.path.dirname(__file__), 'static/uploads'),
                                  endpoint='static',
                                  url_relative_path='uploads/')
        }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash('Login required.', 'warning')
        return redirect(url_for('login'))

    def __init__(self, model, session=None, **kwargs):
        super(ProjectView, self).__init__(model, session, **kwargs)


adminview = Admin(app, index_view=MyAdminIndexView(name='Dashboard', endpoint='admin'))

adminview.add_view(ProjectView(Project, db.session))
adminview.add_view(ProjectView(User, db.session))

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user and save to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@login_required
@app.route('/admin')
def admin():
    return redirect(url_for('admin.index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/toggle_dark_mode', methods=['POST'])
def toggle_dark_mode():
    session['dark_mode'] = not session.get('dark_mode', False)
    return '', 204

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/")
def index():
    projects = Project.query.all()
    return render_template("index.html", projects=projects)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

