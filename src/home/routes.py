from flask import (Blueprint, render_template,)

home = Blueprint("home", __name__)

@home.route("/")
@home.route("/home")
def homepage():
    return render_template("home.html", title = "Home", current_section = "Home")
