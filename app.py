from src.models import Manga
from src import create_app, db
from src.utils import check_dotenv
import waitress

app = create_app()

if __name__ == "__main__":
    check_dotenv()
    with app.app_context():
        db.create_all()
    waitress.serve(app=app, port=6070)
