from flask import (Blueprint, render_template, flash, request)
from src.settings.forms import SettingsForm
from src import db
import os
import json

settings = Blueprint("settings", __name__, url_prefix="/settings")

def create_json_files():
    if not os.path.exists("json"):
        os.mkdir("json")
    if not os.path.exists("json/settings.json"):
        with open("json/settings.json", "w") as f:
            json.dump({}, f)


@settings.route("", methods=["POST", "GET"])
def settingspage():
    with open("json/settings.json", "r") as f:
        json_settings = json.load(f)
    form = SettingsForm()
    if form.validate_on_submit():
        json_settings["theme"] = form.theme.data
        with open("json/settings.json", "w") as f:
            json.dump(json_settings, f, indent=4)
        flash("Settings Updated!", "success")
    elif request.method == "GET":
        form.theme.data = json_settings["theme"]
    return render_template("settings.html", form=form, legend = "Settings", title = "Settings", current_section = "Settings")
