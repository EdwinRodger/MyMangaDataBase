from flask import Blueprint, flash, redirect, render_template, request, url_for
import json

from src.settings.forms import SettingsForm
from src.utils import read_settings

setting = Blueprint("setting", __name__)


# Home Page
@setting.route("/settings", methods=["GET", "POST"])
def settings():
    setting = read_settings()
    form = SettingsForm()
    if form.validate_on_submit():
        setting["UserInterface"]["default_status_to_show"] = str(
            form.default_status_to_show.data
        )
        setting["UserInterface"]["show_cover"] = str(form.show_cover.data)
        setting["UserInterface"]["show_score"] = str(form.show_score.data)
        setting["UserInterface"]["show_volume"] = str(form.show_volume.data)
        setting["UserInterface"]["show_chapter"] = str(form.show_chapter.data)
        setting["UserInterface"]["show_start_date"] = str(form.show_start_date.data)
        setting["UserInterface"]["show_end_date"] = str(form.show_end_date.data)
        setting["UserInterface"]["show_status"] = str(form.show_status.data)
        setting["FlashMessages"]["show_star_on_github"] = str(
            form.show_star_on_github.data
        )
        with open("settings.json", "w", encoding="UTF-8") as settings_file:
            json.dump(setting, settings_file)
        flash("Your settings has been updated!", "success")
        if setting["UserInterface"]["default_status_to_show"] == "All":
            return redirect(url_for("main.home"))
        return redirect(
            url_for(
                "mangas.sort_manga",
                status_value=setting["UserInterface"]["default_status_to_show"],
            )
        )
    if request.method == "GET":
        form.default_status_to_show.data = setting["UserInterface"][
            "default_status_to_show"
        ]
        form.show_cover.data = setting["UserInterface"]["show_cover"]
        form.show_score.data = setting["UserInterface"]["show_score"]
        form.show_volume.data = setting["UserInterface"]["show_volume"]
        form.show_chapter.data = setting["UserInterface"]["show_chapter"]
        form.show_start_date.data = setting["UserInterface"]["show_start_date"]
        form.show_end_date.data = setting["UserInterface"]["show_end_date"]
        form.show_status.data = setting["UserInterface"]["show_status"]
        form.show_star_on_github.data = setting["FlashMessages"]["show_star_on_github"]
    return render_template(
        "settings.html", title="Settings", legend="Settings", form=form
    )
