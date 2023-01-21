# MyMangaDataBase

One database to keep a track of all your mangas.

MyMangaDataBase (or MMDB for short) is

- Free
- Private
- Open source and
- Self Hosted application to track all your mangas.

MMDB backend is made using Python(Flask) with HTML, CSS(Bootstrap) and Jinja used as front-end.

## Features

- [x] Add Manga
- [ ] APIs to edit manga remotely
- [ ] Better UI
- [ ] Cross Platform (Currently works on Windows and Linux(tested using [WSL](https://learn.microsoft.com/en-us/windows/wsl/about)))
- [x] Customizable
- [x] Dark Theme
- [ ] Export to MMDB, ~~MAL, AniList and Kitsu~~
- [x] FOSS
- [ ] Import from MMDB, MAL, ~~AniList and Kitsu~~
- [x] Responsive UI
- [x] Self Hosted
- [x] Show Manga Cover
- [x] Sorted Manga Categories

## How To Use

- Install python 3.10 for [Windows](https://www.python.org/downloads/release/python-3101/) or [Linux](https://tecadmin.net/how-to-install-python-3-10-on-ubuntu-debian-linuxmint/) based on your OS
- Install source code from latest [release](https://github.com/EdwinRodger/MyMangaDataBase/releases/latest) (MyMangaDataBase-{version}.zip)
- Extract the files from the zip folder
- To run MMDB, Simply run `app_runner.py` file
- This will automatically install pipenv and other required packages.
- MyMangaDataBase will open on your default browser.

## Want to Contribute?

See [CONTRIBUTING.md](.github/CONTRIBUTING.md)

MyMangaDataBase is made in [python 3.10](https://www.python.org/downloads/release/python-3101/) and can be run on python>=3.8

You can download the repository by going into 'Code' and then clicking 'Download ZIP' or just click [here](https://github.com/EdwinRodger/MyMangaDataBase/archive/refs/heads/main.zip) to download the same zip file

If you have [git](https://git-scm.com/) installed on your device, you can clone the github repository by running the command below into your terminal -

```git
git clone https://github.com/EdwinRodger/MyMangaDataBase.git
```

Run `app_runner.py` to run the app. It will -
1. Install [pipenv](https://pipenv.pypa.io/en/latest/) package if not already installed
2. Make virtual environment using pipenv
3. Install other packages in that virtual environment if not already installed
4. Automatically run the app on port 6070 in default browser

Alternatively -
1. Run command `app_runner.py --development`
2. Open `http://127.0.0.1:6070/` in browser

## TLDR

To run the code perfectly, you can use any python version between 3.8 to 3.10 and this project is made in python version 3.10.1

I tested MMDB on WSL which is basically linux environment in windows and the program is working fine on my end but I expect it to be buggy or worst, completly broken on actual linux system. If thats the case, open an issue on github and I will try to fix it.

I used mangaupdates.com website to scrape a little bit of data like description, author name, genre etc. You can find the code [here](/src/manga/web_scraper.py)

I didn't learned javascript yet and that is why this project doesn't have js in it and every function is done in python
