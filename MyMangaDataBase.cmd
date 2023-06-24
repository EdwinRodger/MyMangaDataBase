python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
start "" "http://127.0.0.1:6070"
python app.py