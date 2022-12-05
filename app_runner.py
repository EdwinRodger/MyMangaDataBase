import os

try:
    if os.path.exists("Pipfile"):
        if os.path.exists("Pipfile.lock"):
            print("pipenv run app.py")
            os.system("pipenv run app.py")
        else:
            print("pip install pipenv")
            os.system("pip install pipenv")
        print("pipenv install")
        os.system("pipenv install")
        print("pipenv run app.py")
        os.system("pipenv run app.py")
except Exception as e:
    print(e)
    os.system("pause")
