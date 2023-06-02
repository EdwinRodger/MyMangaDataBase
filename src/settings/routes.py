from flask import (Blueprint, render_template,)

settings = Blueprint("settings", __name__, url_prefix="/settings")

@settings.route("")
def settingspage():
    return render_template("settings.html", title = "Settings", current_section = "Settings")
