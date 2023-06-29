from src import db


class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cover = db.Column(db.String, nullable=False, default="default-manga.svg")
    title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    volume = db.Column(db.Integer)
    chapter = db.Column(db.Integer)
    score = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False, default="Plan to read")
    description = db.Column(db.String)
    genre = db.Column(db.String)
    tags = db.Column(db.String)
    author = db.Column(db.String)
    artist = db.Column(db.String)
    notes = db.Column(db.String)

    def __repr__(self):
        return f"Manga('{self.title}', '{self.start_date}', '{self.end_date}', '{self.score}', '{self.status}', '{self.genre}')"


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cover = db.Column(db.String, nullable=False, default="default-anime.svg")
    title = db.Column(db.String, nullable=False)
    episode = db.Column(db.Integer)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    score = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False, default="Plan to watch")
    description = db.Column(db.String)
    genre = db.Column(db.String)
    tags = db.Column(db.String)
    notes = db.Column(db.String)

    def __repr__(self):
        return f"Anime('{self.title}', '{self.start_date}', '{self.end_date}', '{self.score}', '{self.status}', '{self.genre}')"
