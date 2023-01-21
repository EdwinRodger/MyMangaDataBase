import logging
import sys
from webbrowser import open_new_tab

import waitress
from paste.translogger import TransLogger

from src import create_app, db
from src.config import check_config
from src.main.utils import delete_export
from src.models import Manga
from src.utils import check_for_update

app = create_app()

logger = logging.getLogger("waitress")
logger.setLevel(logging.CRITICAL)


def checks():
    check_config()
    try:
        check_for_update()
    except:
        pass
    delete_export()
    with app.app_context():
        db.create_all()


def run_app():
    if "--development" in sys.argv:
        app.run(port=6070, debug=True)
        quit(0)
    print("\nopening http://127.0.0.1:6070\n")
    open_new_tab("http://127.0.0.1:6070")
    if "--logging" in sys.argv:
        waitress.serve(
            TransLogger(app, setup_console_handler=False), host="127.0.0.1", port=6070
        )
    else:
        waitress.serve(app=app, host="127.0.0.1", port=6070)


if __name__ == "__main__":
    checks()
    run_app()
