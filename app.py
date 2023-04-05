import logging
import os
import sys
import threading
from webbrowser import open_new_tab

import waitress
from flask_ngrok2 import run_with_ngrok
from paste.translogger import TransLogger

from src import create_app, db
from src.config import check_settings_json
from src.main.backup import automatic_backup, delete_export
from src.utils import check_for_update

app = create_app()

logger = logging.getLogger("waitress")
logger.setLevel(logging.CRITICAL)


def checks():
    check_settings_json()
    try:
        check_for_update()
    except:
        pass
    delete_export()
    with app.app_context():
        automatic_backup()
        db.create_all()


def run_app():
    if "--development" in sys.argv:
        app.run(port=6070, debug=True)
        sys.exit(0)
    if "--run_with_ngrok" in sys.argv:
        run_with_ngrok(app=app)
        app.run()
        sys.exit(0)
    if "--run_with_localhost" in sys.argv:

        def host():
            waitress.serve(app=app, host="127.0.0.1", port=6070)

        def localhost():
            os.system("ssh -R 80:127.0.0.1:6070 nokey@localhost.run")

        thread1 = threading.Thread(target=host)
        thread2 = threading.Thread(target=localhost)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        sys.exit(0)
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
