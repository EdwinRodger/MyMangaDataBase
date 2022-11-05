# MyMangaDataBase

One database to keep a track of all your mangas

## Features

- [x] Add Manga
- [ ] Add Manga Cover
- [ ] Better UI
- [x] Dark Theme
- [ ] Export [~~MMDB~~, MAL, AniList and Kitsu]
- [x] FOSS
- [ ] Import [~~MMDB~~, MAL, AniList and Kitsu]
- [x] Responsive UI
- [x] Sorting Mangas

## How To Use

- Install [python](https://www.python.org/downloads/release/python-3108/) for your respective OS
- Install source code from latest [release](https://github.com/EdwinRodger/MyMangaDataBase/releases/latest)
- To run MMDB on Windows, Simply run `MyMangaDataBase.bat` file.
- To run MMBD on MacOS or Linux -
  
  - Option 1 -
    1. Run `MyMangaDataBase.sh` file
  
  - Option 2 -
    1. Open terminal in MyMangaDataBase folder
    2. In terminal, write `python3 app_runner.py`
    - If `app_runner.py` file fails, you can debug and correct it and if you want, you can make a pull request so that other people can run the application without any problem

  - Option 3 -
    1. Open terminal in MyMangaDataBase folder
    2. Enter command `pip3 install pipenv` (Do this only when running the program for the first time)
    3. Then enter command `pipenv run app.py` to run the program

- This will install pipenv package and automatically install other required packages.
- MyMangaDataBase will open on your default browser.

## Want to Contribute?

MyMangaDataBase is made in [python 3.10](https://www.python.org/downloads/release/python-3101/)

You can download the repository by going into 'Code' and then clicking 'Download ZIP' or just click [here](https://github.com/EdwinRodger/MyMangaDataBase/archive/refs/heads/main.zip) to download the same zip file

Don't want to download the code? No worries!

If you have [git](https://git-scm.com/) installed on your device, you can clone the github repository by running the command below into your terminal -

```git
git clone https://github.com/EdwinRodger/MyMangaDataBase.git
```

If not already installed, install [pipenv](https://pipenv.pypa.io/en/latest/) package for making virtual environment -

```python
pip install pipenv
```

then download the required packages from Pipfile -

```python
pipenv install
```

and after that you are ready to make a software changing commit
