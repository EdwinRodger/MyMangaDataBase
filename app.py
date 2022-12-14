import logging
from webbrowser import open_new_tab

import waitress

from src import create_app, db
from src.main.utils import delete_export
from src.models import Manga
from src.utils import check_dotenv, check_for_update

app = create_app()
logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    check_dotenv()
    try:
        check_for_update()
    except:
        pass
    delete_export()
    with app.app_context():
        db.create_all()
    print("\nopening http://127.0.0.1:6070\n")
    open_new_tab("http://127.0.0.1:6070")
    waitress.serve(app=app, host="127.0.0.1", port=6070)
