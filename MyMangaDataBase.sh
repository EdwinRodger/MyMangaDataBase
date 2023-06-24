python3 -m venv venv
call venv\Scripts\activate
pip3 install -r requirements.txt
start "" "http://127.0.0.1:6070"
python3 app.py