import json
import logging
import sys
from time import strftime

import waitress
from flask import request

from src import create_app, db
from src.anime.backup import delete_anime_export
from src.home.utils import check_for_update
from src.manga.backup import delete_manga_export
from src.settings.routes import create_json_files

app = create_app()


# This custom logging is taken from https://gist.github.com/alexaleluia12/e40f1dfa4ce598c2e958611f67d28966#file-flask_logging_requests-py-L28
@app.after_request
def after_request(response):
    timestamp = strftime("[%Y-%b-%d %H:%M]")
    logger.info(
        "%s %s %s %s %s %s",
        timestamp,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        response.status,
    )
    return response


def checks():
    with app.app_context():
        db.create_all()
    create_json_files()
    check_for_update()
    delete_anime_export()
    delete_manga_export()


def run():
    if sys.argv[-1].lower() == "super-saiyan":
        app.run(host="127.0.0.1", port=6070, debug=True)
    else:
        waitress.serve(app=app, host="127.0.0.1", port=6070)


if __name__ == "__main__":
    checks()
    with open("json/settings.json", "r") as f:
        settings = json.load(f)
    logger = logging.getLogger("tdm")
    if settings["enable_logging"] == "Yes":
        logger.setLevel(logging.INFO)
    run()
