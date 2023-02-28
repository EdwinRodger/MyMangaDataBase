import waitress

from src import create_app

app = create_app()

def run_app():
    waitress.serve(app=app, host="127.0.0.1", port=6070)


if __name__ == "__main__":
    run_app()
