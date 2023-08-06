from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class SettingsForm(FlaskForm):
    theme = SelectField("Theme", choices=["Dark", "Light"])
    enable_logging = SelectField("Enable Logging", choices=["Yes", "No"])
    truncate_title = SelectField("Truncate Title", choices=["Yes", "No"])
    layout = SelectField("Layout", choices=["Table", "Card"])
    save = SubmitField("Save")
