# MyMangaDataBase

![Home Page](docs/images/2023-06-24/hero(2023-06-24).png "Home Page")

One database to keep track of your Anime and Manga.

MyMangaDataBase (or MMDB for short) is

- Free
- Private
- Open source
- Self Hosted application to track all your anime and manga.

Use MMDB to make your own Anime and Manga list without the fear of a certain manga/anime not present in your tracking site's database. MMDB is a self-hosted option which means all the data remains on your device.

MMDB backend is made using Python(Flask) with HTML, CSS(Bootstrap5) and Jinja used as front-end.

Try demo at https://mymangadatabase.pythonanywhere.com/

## Features

- Dark Theme
- Editable metadata (genre, description etc.)
- Export to MMDB
- Import from
  - AniList (Anime & Manga)
  - MangaUpdates (Manga)
  - MyAnimeList (Anime & Manga)
  - MMDB (Anime & Manga)
- Responsive UI
- Self Hosted
- Sort by status
- Search by genre or tags

## Road Map

- Make APIs

## How To Use

### For Windows

1. Install latest MMDB version from releases page.
2. Extract and open zip file
3. Run MyMangaDataBase.exe

### For Linux (Tested using [WSL](https://learn.microsoft.com/en-us/windows/wsl/about))

1. Install [Python](https://python.org) and [Git](https://git-scm.com) if not already installed
2. Install pipenv ([How to install](https://github.com/pypa/pipenv?tab=readme-ov-file#installation))
3. Clone repo or download MyMangaDataBase-{version}-linux from [latest releases](https://github.com/EdwinRodger/MyMangaDataBase/releases/latest)
4. Run - `cd ./MyMangaDataBase-{version}-linux/MyMangaDataBase-main`
5. Run - `pipenv install`
6. Run - `pipenv run ./app.py` or `pipenv run python3 ./app.py`

## Host on pythonanywhere.org

1. Make an account on pythonanywhere.org
2. Using console, git clone `https://github.com/EdwinRodger/MyMangaDataBase.git`
3. In Files tab, goto MyMangaDataBase folder, then click on 'Open Bash Console here'
4. Run - `pip3 install -r requirements.txt`
5. In Web tab, under Code section change 'Source Code' and 'Working Directory' to `/home/MyMangaDataBase/MyMangaDataBase`
6. Reload your webapp
7. It should get hosted on your-username.pythonanywhere.org 

## Want to Contribute?

See [CONTRIBUTING.md](.github/CONTRIBUTING.md)

MyMangaDataBase is made in [python 3.10](https://www.python.org/downloads/release/python-3101/) and can be run on python>=3.8

You can download the repository by going into 'Code' and then clicking 'Download ZIP' or just click [here](https://github.com/EdwinRodger/MyMangaDataBase/archive/refs/heads/main.zip) to download the same zip file

If you have [git](https://git-scm.com/) installed on your device, you can clone the github repository by running the command below into your terminal -

```git
git clone https://github.com/EdwinRodger/MyMangaDataBase.git
```

1. Run command `python app.py` (Make sure you are in virtual environement).
2. Open `http://127.0.0.1:6070/` in browser

## Debugging

Pass `super-saiyan` argument while running `app.py`, it will turn on flask debugging.

## TLDR

To run the code perfectly, you can use any python version between 3.8 to 3.10 and this project is made in python version 3.10.1

I tested MMDB on WSL which is basically linux environment in windows and the program is working fine on my end but I expect it to be buggy or worst, completly broken on actual linux system. If thats the case, open an issue on github and I will try to fix it.

I used [jikan.moe](https://jikan.moe) api to get manga details. You can find the code [here](https://github.com/EdwinRodger/MyMangaDataBase/blob/48cde5db4b2e033b7164faad06c1a1baef9d2f4a/src/manga/backup.py#L115). To lower the load on server, there is a [1 second sleep](https://github.com/EdwinRodger/MyMangaDataBase/blob/48cde5db4b2e033b7164faad06c1a1baef9d2f4a/src/manga/backup.py#L185) between requests.

I didn't learned javascript yet and that is why this project doesn't have any JS in it and every function is done in python using routes. If you find any javascript, I most probably copied it from stackoverflow or documentations.
