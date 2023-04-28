# Python Imports
import errno
import logging
import os
import sys
import threading
from typing import Optional
from webbrowser import open_new_tab

# Third Party Imports
import flask_ngrok2
import waitress
from paste.translogger import TransLogger
from rich import print as richprint

# Custom Imports
from src import create_app, db
from src.config import check_chapterlog_json, check_settings_json
from src.main.backup import automatic_backup, delete_export
from src.utils import check_for_update

# Installing typer package
try:
    import typer
except ModuleNotFoundError:
    print("typer module not found!")
    print("Installing typer")
    os.system("pip install typer[all]")
    import typer

# Creating app from src directory
app = create_app()
# Getting waitress logger if user wants to turn on logger, Source: https://docs.pylonsproject.org/projects/waitress/en/stable/logging.html#logging-to-the-console-using-python
logger = logging.getLogger("waitress")
logger.setLevel(logging.CRITICAL)


# Checks before running the MMDB
def checks():
    # Checks for settings.json
    check_settings_json()
    # Checks for chapter-log.json
    check_chapterlog_json()
    # Checks for MMDB update
    try:
        check_for_update()
    except:
        pass
    # Deletes previous exports
    delete_export()
    # Creating database
    with app.app_context():
        # Automatic backup every sunday
        automatic_backup()
        db.create_all()


# Current Version
VERSION = "1.7.0"


# Function used by typer
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
    # Prints Version
    if version:
        richprint(VERSION)
        sys.exit(0)
    # Runs flask development environment
    if development:
        app.run(port=6070, debug=True)
        sys.exit(0)
    # Runs the server with ngrok
    if run_with_ngrok:
        # Give warnings
        richprint(
            "[red]Running with ngrok requires you to have ngrok installed, configured with authtoken and set to path otherwise your server won't run!"
        )
        # Give input
        var = str(input("Do you want to continue?[(Y)es/(N)o] "))
        # Check input
        if var.lower().startswith("y"):
            # If the input is yes then run the server with ngrok
            flask_ngrok2.run_with_ngrok(app=app)
            app.run()
            sys.exit(0)
    # Runs the server on localhost.run
    if run_with_localhost:
        richprint(
            "[red]Running with localhost.run will have slower loading and server url will last only one hour"
        )
        # Give input
        var = str(input("Do you want to continue?[(Y)es/(N)o] "))
        # Check input
        if var.lower().startswith("y"):
            # Making two functions for threading. One will run server and one will connect to localhost.run
            # Creating server
            def host():
                waitress.serve(app=app, host="127.0.0.1", port=6070)

            # Connecting the server to localhost.run using ssh
            def localhost():
                os.system("ssh -R 80:127.0.0.1:6070 nokey@localhost.run")

            # Running the server and connection simultaneously
            thread1 = threading.Thread(target=host)
            thread2 = threading.Thread(target=localhost)
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
            sys.exit(0)
    # Checking for pipfile
    if os.path.exists("Pipfile"):
        # Checking for pipfile.lock
        # If pipfile.lock doesn't exists then install packages from pipfile
        if not os.path.exists("Pipfile.lock"):
            # Informing user about installation of pipenv
            richprint(
                "\nInstalling [green]pipenv[/green] to make virtual environment\n"
            )
            # Installing pipenv
            os.system("pip install pipenv")
            # Informing user about making of virtual environment
            richprint(
                "\nCreating [green]virtual environment[/green] and installing required packages from pipfile via pipenv\n"
            )
            # Making virtual environment and installing required packages
            os.system("pipenv install")
        richprint(
            f"Starting MyMangaDataBase [green]{VERSION}[/green]! Please wait...\n"
        )
        # Opening localhost on port 6070
        richprint("\nopening http://127.0.0.1:6070\n")
        open_new_tab("http://127.0.0.1:6070")
        # If logging in cli arguments then turning on logger
        if logging:
            waitress.serve(
                TransLogger(app, setup_console_handler=False),
                host="127.0.0.1",
                port=6070,
            )
        # Runing server
        else:
            waitress.serve(app=app, host="127.0.0.1", port=6070)
        sys.exit(0)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Pipfile")


if __name__ == "__main__":
    checks()
    typer.run(mmdb_cli)
