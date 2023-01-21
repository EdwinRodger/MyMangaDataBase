from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class MangaForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    cover = FileField("Cover Image", validators=[FileAllowed(["jpg", "png"])])
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    volume = IntegerField("Volume")
    chapter = IntegerField("Chapter")
    score = SelectField("Score", choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    status = SelectField(
        "Status",
        choices=[
            "Reading",
            "Completed",
            "On hold",
            "Dropped",
            "Plan to read",
            "Rereading",
        ],
    )
    submit = SubmitField("Add")
    update = SubmitField("Update")


class SearchBar(FlaskForm):
    search_field = StringField("Search", validators=[DataRequired(), Length(min=2)])
    search_button = SubmitField("Search")
