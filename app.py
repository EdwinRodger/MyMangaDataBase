from src.models import Manga
from src import create_app, db
from src.utils import check_dotenv
import waitress
import logging

app = create_app()
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    check_dotenv()
    with app.app_context():
        db.create_all()
    waitress.serve(app=app, host='127.0.0.1', port=6070)
