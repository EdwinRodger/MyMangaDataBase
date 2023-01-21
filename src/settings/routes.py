from configparser import ConfigParser

from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.settings.forms import SettingsForm

setting = Blueprint("setting", __name__)

# Home Page
@setting.route("/settings", methods=["GET", "POST"])
def settings():
    file = "config.ini"
    config = ConfigParser()
    config.read(file)
    form = SettingsForm()
    if form.validate_on_submit():
        config["UserInterface"]["default_status_to_show"] = str(
            form.default_status_to_show.data
        )
        config["UserInterface"]["show_cover"] = str(form.show_cover.data)
        config["UserInterface"]["show_score"] = str(form.show_score.data)
        config["UserInterface"]["show_volume"] = str(form.show_volume.data)
        config["UserInterface"]["show_chapter"] = str(form.show_chapter.data)
        config["UserInterface"]["show_start_date"] = str(form.show_start_date.data)
        config["UserInterface"]["show_end_date"] = str(form.show_end_date.data)
        config["UserInterface"]["show_status"] = str(form.show_status.data)
        with open(file, "w") as cf:
            config.write(cf)
        flash("Your settings has been updated!", "success")
        if config["UserInterface"]["default_status_to_show"] == "All":
            return redirect(url_for("main.home"))
        else:
            return redirect(
                url_for(
                    "mangas.sort_manga",
                    sort_func=config["UserInterface"]["default_status_to_show"],
                )
            )

    elif request.method == "GET":
        form.default_status_to_show.data = config["UserInterface"][
            "default_status_to_show"
        ]
        form.show_cover.data = config["UserInterface"]["show_cover"]
        form.show_score.data = config["UserInterface"]["show_score"]
        form.show_volume.data = config["UserInterface"]["show_volume"]
        form.show_chapter.data = config["UserInterface"]["show_chapter"]
        form.show_start_date.data = config["UserInterface"]["show_start_date"]
        form.show_end_date.data = config["UserInterface"]["show_end_date"]
        form.show_status.data = config["UserInterface"]["show_status"]
    return render_template(
        "settings.html", title="Settings", legend="Settings", form=form
    )
