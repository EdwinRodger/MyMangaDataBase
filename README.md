# MyMangaDataBase

![Home Page](docs/images/hero(2023-06-24).png "Home Page")

One database to keep track of your Anime and Manga.

MyMangaDataBase (or MMDB for short) is

- Free
- Private
- Open source and
- Self Hosted application to track all your anime and manga.

Use MMDB to make your own Anime and Manga list without the fear of a certain manga/anime not present in your tracking site's database. MMDB is a self-hosted option which means all the data remains on your device.

MMDB backend is made using Python(Flask) with HTML, CSS(Bootstrap5) and Jinja used as front-end.

Try demo at https://mymangadatabase.pythonanywhere.com/

## Features

<!-- - Customizable -->
- Dark Theme
- Editable metadata (genre, description etc.)
- Export to MMDB
- Import from MyAnimeList, MMDB
- Responsive UI
- Self Hosted
- Sort by status
- Search by genre or tags

## Road Map

- Cross Platform (Currently works on Windows and Linux(tested using [WSL](https://learn.microsoft.com/en-us/windows/wsl/about)))
- Export to MAL, Anilist, Kitsu and other services
- Import from Anilist, Kitsu and other services
- Simple routes to edit manga remotely

## How To Use

- Install python 3.10 for [Windows](https://www.python.org/downloads/release/python-3101/) or [Linux](https://tecadmin.net/how-to-install-python-3-10-on-ubuntu-debian-linuxmint/) based on your OS
- Install source code from latest [release](https://github.com/EdwinRodger/MyMangaDataBase/releases/latest) (MyMangaDataBase-{version}.zip)
- Extract the files from the zip folder
- To run MMDB, Simply run `MyMangaDataBase.cmd`(Windows) or `MyMangaDataBase.sh`(Linux) depending on your OS. This will -
    - Automatically make virtual environment
    - Install all required packages in it
    - MyMangaDataBase will open on your default browser


## Want to Contribute?

See [CONTRIBUTING.md](.github/CONTRIBUTING.md)

MyMangaDataBase is made in [python 3.10](https://www.python.org/downloads/release/python-3101/) and can be run on python>=3.8

You can download the repository by going into 'Code' and then clicking 'Download ZIP' or just click [here](https://github.com/EdwinRodger/MyMangaDataBase/archive/refs/heads/main.zip) to download the same zip file

If you have [git](https://git-scm.com/) installed on your device, you can clone the github repository by running the command below into your terminal -

```git
git clone https://github.com/EdwinRodger/MyMangaDataBase.git
```

Run `MyMangaDataBase.cmd/sh` to run the app. It will -
1. Make virtual environment
2. Install other packages in that virtual environment if not already installed
3. Automatically run the app on port 6070 in default browser

Alternatively -
1. Run command `app.py super-saiyan` (Make sure you are in virtual environement), This will give MMDB god-like powers like debugging.
2. Open `http://127.0.0.1:6070/` in browser

## TLDR

To run the code perfectly, you can use any python version between 3.8 to 3.10 and this project is made in python version 3.10.1

I tested MMDB on WSL which is basically linux environment in windows and the program is working fine on my end but I expect it to be buggy or worst, completly broken on actual linux system. If thats the case, open an issue on github and I will try to fix it.

I used [jikan.moe](https://jikan.moe) api to get manga details. You can find the code [here](https://github.com/EdwinRodger/MyMangaDataBase/blob/48cde5db4b2e033b7164faad06c1a1baef9d2f4a/src/manga/backup.py#L115). To lower the load on server, there is a [1 second sleep](https://github.com/EdwinRodger/MyMangaDataBase/blob/48cde5db4b2e033b7164faad06c1a1baef9d2f4a/src/manga/backup.py#L185) between requests.

I didn't learned javascript yet and that is why this project doesn't have any JS in it and every function is done in python using routes. If you find any javascript, I most probably copied it from stackoverflow or documentations.
