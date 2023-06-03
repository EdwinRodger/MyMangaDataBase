from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class SettingsForm(FlaskForm):
    theme = SelectField("Theme", choices=["Dark", "Light"])
    save = SubmitField("Save")
    