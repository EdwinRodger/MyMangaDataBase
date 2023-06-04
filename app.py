from src import create_app, db
from src.settings.routes import create_json_files
from src.home.utils import check_for_update

app = create_app()

def run():
    with app.app_context():
        db.create_all()
    create_json_files()
    check_for_update()
    app.run(port=6070, debug=True)

if __name__ == "__main__":
    run()