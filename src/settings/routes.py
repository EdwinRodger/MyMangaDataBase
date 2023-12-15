import json
import os

from flask import Blueprint, flash, render_template, request

from src import db
from src.settings.forms import SettingsForm

settings = Blueprint("settings", __name__, url_prefix="/settings")


def create_json_files():
    if not os.path.exists("json"):
        os.mkdir("json")
    if not os.path.exists("json/settings.json"):
        with open("json/settings.json", "w") as f:
            settings = {
                "theme": "Dark",
                "enable_logging": "Yes",
                "truncate_title": "No",
                "layout": "Table",
                "mmdb_promotion": "Yes",
            }
            json.dump(settings, f)
    if not os.path.exists("json/mangalogs.json"):
        with open("json/mangalogs.json", "w") as f:
            json.dump({}, f)
    if not os.path.exists("json/animelogs.json"):
        with open("json/animelogs.json", "w") as f:
            json.dump({}, f)


@settings.route("", methods=["POST", "GET"])
def settingspage():
    with open("json/settings.json", "r") as f:
        json_settings = json.load(f)

    form = SettingsForm()

    if form.validate_on_submit():
        # Theme
        json_settings["theme"] = form.theme.data
        # Logging
        json_settings["enable_logging"] = form.enable_logging.data
        # Truncate Title
        json_settings["truncate_title"] = form.truncate_title.data
        # Layout
        json_settings["layout"] = form.layout.data
        # MMDB Promotion
        json_settings["mmdb_promotion"] = form.mmdb_promotion.data

        with open("json/settings.json", "w") as f:
            json.dump(json_settings, f, indent=4)
        flash("Settings Updated!", "success")
    elif request.method == "GET":
        # Theme
        form.theme.data = json_settings["theme"]
        # Enable Logging
        form.enable_logging.data = json_settings["enable_logging"]
        # Truncate Title
        form.truncate_title.data = json_settings["truncate_title"]
        # Layout
        form.layout.data = json_settings["layout"]
        # MMDB Promotion
        form.mmdb_promotion.data = json_settings["mmdb_promotion"]
    return render_template(
        "settings.html",
        form=form,
        legend="Settings",
        title="Settings",
        current_section="Settings",
    )
