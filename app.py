import logging
import os
from webbrowser import open_new_tab

import waitress

from src import create_app, db
from src.models import Manga
from src.utils import check_dotenv
from src.main.utils import delete_export

app = create_app()
logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    check_dotenv()
    delete_export()
    with app.app_context():
        db.create_all()
    os.system("echo opening http://127.0.0.1:6070")
    open_new_tab("http://127.0.0.1:6070")
    waitress.serve(app=app, host="127.0.0.1", port=6070)
