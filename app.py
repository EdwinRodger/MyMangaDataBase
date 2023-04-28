import errno
import logging
import os
import sys
import threading
from typing import Optional
from webbrowser import open_new_tab

import flask_ngrok2
import waitress
from paste.translogger import TransLogger
from rich import print as richprint

from src import create_app, db
from src.config import check_chapterlog_json, check_settings_json
from src.main.backup import automatic_backup, delete_export
from src.utils import check_for_update

try:
    import typer
except ModuleNotFoundError:
    print("typer module not found!")
    print("Installing typer")
    os.system("pip install typer[all]")
    import typer


app = create_app()

logger = logging.getLogger("waitress")
logger.setLevel(logging.CRITICAL)


def checks():
    check_settings_json()
    check_chapterlog_json()
    try:
        check_for_update()
    except:
        pass
    delete_export()
    with app.app_context():
        automatic_backup()
        db.create_all()


VERSION = "1.7.0"


def mmdb_cli(
    version: Optional[bool] = typer.Option(
        None,
        "--version/ ",
        help="Show current version of the program and exit.",
    ),
    development: Optional[bool] = typer.Option(
        None,
        "--development/ ",
        help="Turns on Flask development environment and debugger.",
        rich_help_panel="For Devs",
    ),
    logging: Optional[bool] = typer.Option(
        None,
        "--logging/ ",
        help="Show logs in terminal in the Apache Combined Log Format for that session.",
        rich_help_panel="For Devs",
    ),
    run_with_ngrok: Optional[bool] = typer.Option(
        None,
        "--run-with-ngrok/ ",
        help="Runs your host on ngrok which helps you to access your database from other devices.",
        rich_help_panel="Hosting",
    ),
    run_with_localhost: Optional[bool] = typer.Option(
        None,
        "--run-with-localhost/ ",
        help="Runs your host on localhost.run which helps you to access your database from other \
        devices.",
        rich_help_panel="Hosting",
    ),
):
    if version:
        richprint(VERSION)
        sys.exit(0)
    if development:
        app.run(port=6070, debug=True)
        sys.exit(0)
    if run_with_ngrok:
        richprint(
            "[red]Running with ngrok requires you to have ngrok installed, configured with authtoken and set to path otherwise your server won't run!"
        )
        var = str(input("Do you want to continue?[(Y)es/(N)o] "))
        if var.lower().startswith("y"):
            flask_ngrok2.run_with_ngrok(app=app)
            app.run()
            sys.exit(0)
    if run_with_localhost:
        richprint(
            "[red]Running with localhost.run will have slower loading and server url will last only one hour"
        )
        var = str(input("Do you want to continue?[(Y)es/(N)o] "))
        if var.lower().startswith("y"):

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
    if os.path.exists("Pipfile"):
        if not os.path.exists("Pipfile.lock"):
            richprint(
                "\nInstalling [green]pipenv[/green] to make virtual environment\n"
            )
            os.system("pip install pipenv")
            richprint(
                "\nCreating [green]virtual environment[/green] and installing required packages from pipfile via pipenv\n"
            )
            os.system("pipenv install")
        richprint(
            f"Starting MyMangaDataBase [green]{VERSION}[/green]! Please wait...\n"
        )
        richprint("\nopening http://127.0.0.1:6070\n")
        open_new_tab("http://127.0.0.1:6070")
        if logging:
            waitress.serve(
                TransLogger(app, setup_console_handler=False),
                host="127.0.0.1",
                port=6070,
            )
        else:
            waitress.serve(app=app, host="127.0.0.1", port=6070)
        sys.exit(0)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Pipfile")

if __name__ == "__main__":
    checks()
    typer.run(mmdb_cli)
