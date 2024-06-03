import platform

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional


class MangaForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    cover = FileField("Cover Image", validators=[FileAllowed(["jpg", "png"])])
    if platform.system() == "Windows":
        start_date = DateField("Start Date")
        end_date = DateField("End Date")
    else:
        # DateField will allow None which is a Linux specific problem, solved using - https://github.com/wtforms/wtforms/issues/489#issuecomment-1382074627
        start_date = DateField("Start Date", validators=[Optional()])
        end_date = DateField("End Date", validators=[Optional()])
    volume = IntegerField("Volume")
    chapter = IntegerField("Chapter")
    score = SelectField("Score", choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    status = SelectField(
        "Status",
        choices=["Reading", "Completed", "On hold", "Dropped", "Plan to read"],
    )
    description = TextAreaField("Description")
    genre = StringField("Genre")
    tags = StringField("Tags")
    author = StringField("Author")
    artist = StringField("Artist")
    notes = TextAreaField("Notes")
    submit = SubmitField("Add")
    update = SubmitField("Update")


class MangaSearchBar(FlaskForm):
    search_field = StringField("Search", validators=[DataRequired(), Length(min=2)])
    search_button = SubmitField("Search")
