from src import create_app, db

app = create_app()

def run():
    with app.app_context():
        db.create_all()
    app.run(port=6070, debug=True)

if __name__ == "__main__":
    run()