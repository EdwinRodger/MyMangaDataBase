from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class SettingsForm(FlaskForm):
    default_status_to_show = SelectField(
        "Default Status",
        choices=[
            "All",
            "Reading",
            "Completed",
            "On hold",
            "Dropped",
            "Plan to read",
            "Rereading",
        ],
    )
    show_cover = SelectField("Show Cover", choices=["Yes", "No"])
    show_score = SelectField("Show Score", choices=["Yes", "No"])
    show_volume = SelectField("Show Volume", choices=["Yes", "No"])
    show_chapter = SelectField("Show Chapter", choices=["Yes", "No"])
    show_start_date = SelectField("Show Start Date", choices=["Yes", "No"])
    show_end_date = SelectField("Show End Date", choices=["Yes", "No"])
    show_status = SelectField("Show Status", choices=["Yes", "No"])

    show_star_on_github = SelectField(
        "Show occaisional message asking user to star MMDB on github",
        choices=["Yes", "No"],
    )
    update = SubmitField("Update")
