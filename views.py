from flask_admin.contrib.mongoengine import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user, login_required, login_user, logout_user
from flask import redirect, render_template, abort, session, request, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Project
from app import app
from admin import admin
from flask_admin import Admin
from forms import RegistrationForm

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
    from_override = {
            'image': FileUploadField
            }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash('Login required.', 'warning')
        return redirect(url_for('login'))


admin = Admin(app, index_view=MyAdminIndexView(name='Dashboard', endpoint='admin'))

admin.add_view(ProjectView(Project))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user and save to the database
        new_user = User(username=username, password=hashed_password)
        new_user.save()

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
        user = User.objects(username=username).first()
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
    projects = Project.objects()
    return render_template("index.html", projects=projects)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

