import os
import platform

try:
    if os.path.exists("Pipfile"):
        if os.path.exists("Pipfile.lock"):
            print("pipenv run app.py")
            os.system("pipenv run app.py")
        else:
            if platform.system() == "Windows":
                print("pip install pipenv")
                os.system("pip install pipenv")
            else:
                print("pip3 install pipenv")
                os.system("pip3 install pipenv")
            print("pipenv install")
            os.system("pipenv install")
            print("pipenv run app.py")
            os.system("pipenv run app.py")
except Exception as e:
    print(e)
    if platform.system() == "Windows":
        os.system("pause")
    else:
        os.system("read -p 'Press enter key to resume ...'")
