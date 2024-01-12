from flask import Flask, render_template, abort

app = Flask(__name__)

projects = [
    {
        "name": "NES emulator in rust-lang",
        "thumb": "img/habit-tracking.png",
        "hero": "img/habit-tracking-hero.png",
        "categories": ["rust", "low-level"],
        "slug": "rust",
        "prod": "https://nes.evenbom.se/"
    },
]
slug_to_project = {project["slug"]: project for project in projects}

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

if __name__ == "__main__":
    app.run(debug=True)
