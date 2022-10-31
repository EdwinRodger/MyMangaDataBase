from src import db


class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column(db.String, nullable=False, default="default.png")
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    volume = db.Column(db.Integer)
    chapter = db.Column(db.Integer)
    score = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False, default="Plan to read")

    def __repr__(self):
        return f"Manga('{self.title}', '{self.start_date}', '{self.end_date}')"
