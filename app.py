import sys
from webbrowser import open_new_tab

import waitress
from paste.translogger import TransLogger

from src import create_app, db
from src.main.utils import delete_export
from src.models import Manga
from src.utils import check_dotenv, check_for_update

app = create_app()

if __name__ == "__main__":
    check_dotenv()
    try:
        check_for_update()
    except:
        pass
    delete_export()
    with app.app_context():
        db.create_all()
    if "--development" in sys.argv:
        app.run(port=6070, debug=True)
    if len(sys.argv) == 1:
        print("\nopening http://127.0.0.1:6070\n")
        open_new_tab("http://127.0.0.1:6070")
        waitress.serve(
            TransLogger(app, setup_console_handler=False), host="127.0.0.1", port=6070
        )
