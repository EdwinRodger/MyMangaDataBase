from src import create_app, db
from src.settings.routes import create_json_files

app = create_app()

def run():
    with app.app_context():
        db.create_all()
    create_json_files()
    app.run(port=6070, debug=True)

if __name__ == "__main__":
    run()