import os

def check_dotenv():
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(f"SECRET_KEY={os.urandom(60).hex()}\nSQLALCHEMY_DATABASE_URI='sqlite:///manga.db'")