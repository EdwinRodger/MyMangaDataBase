import os
import platform
from webbrowser import open_new_tab

try:
    if os.path.exists("Pipfile"):
        if os.path.exists("Pipfile.lock"):
            open_new_tab("http://127.0.0.1:6070")
            os.system('pipenv run app.py')
        else:
            if platform.system() == 'Windows':
                os.system('pip install pipenv')
            else:
                os.system('pip3 install pipenv')
            os.system('pipenv install')
            open_new_tab("http://127.0.0.1:6070")
            os.system('pipenv run app.py')
except Exception as e:
    os.system(f'echo {e}')
    os.system('pause')