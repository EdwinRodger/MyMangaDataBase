from src.models import Manga
from src import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
