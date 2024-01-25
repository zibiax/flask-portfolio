from flask_admin.contrib.mongoengine import ModelView
from flask_login import current_user
from flask import Flask, render_template, abort, session

from app import app
from app import admin
from models import Project

projects = [
    {
        "name": "NES emulator in rust-lang",
        "thumb": "img/nes.png",
        "hero": "img/nes.png",
        "categories": ["rust", "low-level"],
        "slug": "rust",
        "prod": "https://github.com/zibiax/rusty-nes/"
    },
]
slug_to_project = {project["slug"]: project for project in projects}

@app.route('/toggle_dark_mode', methods=['POST'])
def toggle_dark_mode():
    session['dark_mode'] = not session.get('dark_mode', False)
    return '', 204

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/")
def index():
    return render_template("index.html", projects=projects)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/project/<string:slug>")
def project(slug):
    if slug not in slug_to_project:
        abort(404)
    return render_template(f"project_{slug}.html", project=slug_to_project[slug])

