import os
import platform

try:
    if os.path.exists("Pipfile"):
        if os.path.exists("Pipfile.lock"):
            os.system("echo pipenv run app.py")
            os.system("pipenv run app.py")
        else:
            if platform.system() == "Windows":
                os.system("echo pip install pipenv")
                os.system("pip install pipenv")
            else:
                os.system("echo pip3 install pipenv")
                os.system("pip3 install pipenv")
            os.system("echo pipenv install")
            os.system("pipenv install")
            os.system("echo pipenv run app.py")
            os.system("pipenv run app.py")
except Exception as e:
    os.system(f"echo {e}")
    os.system("pause")
