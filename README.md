# MyMangaDataBase

One database to keep a track of all your mangas. MyMangaDataBase (or MMDB for short) is a free and open source program to track all your mangas. MMDB backend is made using Python and Flask with HTML, CSS and Jinja used as front-end.

## Features

- [x] Add Manga
- [ ] Add Manga Cover
- [ ] Better UI
- [x] Dark Theme
- [ ] Export [~~MMDB~~, MAL, AniList and Kitsu]
- [x] FOSS
- [ ] Import [~~MMDB~~, MAL, AniList and Kitsu]
- [ ] Cross Platform Support (Currently works only on Windows)
- [x] Responsive UI
- [x] Sorting Mangas

## How To Use

- Install [python](https://www.python.org/downloads/release/python-3108/) for Windows OS (Currently unsupported for Mac and Linux systems)
- Install source code from latest [release](https://github.com/EdwinRodger/MyMangaDataBase/releases/latest)
- Extract the files from the zip folder
- To run MMDB, Simply run `app_runner.py` file
- This will automatically install pipenv and other required packages.
- MyMangaDataBase will open on your default browser.

## Want to Contribute?

See [CONTRIBUTING.md](.github/CONTRIBUTING.md)

MyMangaDataBase is made in [python 3.10](https://www.python.org/downloads/release/python-3101/) and can be run on python>=3.8

You can download the repository by going into 'Code' and then clicking 'Download ZIP' or just click [here](https://github.com/EdwinRodger/MyMangaDataBase/archive/refs/heads/main.zip) to download the same zip file

Don't want to download the code? No worries!

If you have [git](https://git-scm.com/) installed on your device, you can clone the github repository by running the command below into your terminal -

```git
git clone https://github.com/EdwinRodger/MyMangaDataBase.git
```

Run `app_runner.py` to run the app. It will -
1. Install [pipenv](https://pipenv.pypa.io/en/latest/) package if not already installed
2. Make virtual environment using pipenv
3. Install other packages in that virtual environment if not already installed
4. Automatically run the app on port 6070 in default browser
