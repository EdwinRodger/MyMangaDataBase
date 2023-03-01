# Changelog

## 1.7.0

### New

- **NEW DEMO SITE!!!** at https://mymangadatabase.pythonanywhere.com/
- An occasional flash message to star MMDB on github and setting to toggle it On or Off
- Arguments -
  - `--run-with-ngrok`, Hosts the server on [ngrok](https://ngrok.com/)
    - Requires ngrok to be installed on the system
    - Requires ngrok account
    - Requires authtoken to be configured by ngrok
  - `--run-with-localhost`, Hosts the server on [localhost.run](https://localhost.run)
    - Load site slowly
- Blueprint: errors, new error pages
- Blueprint: functions, to make simple database operations easier
- `help.md` to help non-technical users with basic things
- Links to github under info section -
  - Bug report
  - Feature request
  - Star MyMangaDataBase
- Packages -
  - [sqlite-web](https://github.com/coleifer/sqlite-web) (dev)
  - [flask-ngrok2](https://github.com/MohamedAliRashad/flask-ngrok2)
  - [pylint](https://pylint.readthedocs.io/en/latest/)
- Rich help panel
- Search by genre
- Three setting sections - 
  - Defaults
  - Column Interface
  - Flash Messages

### Fixed

- Overflowing of metadata content from main div on smaller devices
- Typos

### Updated

- Change `Info` to `Help` in navbar
- Changed `sort_func` variable to `status_value`
- Python Packages
- Rerouting to same manga page after updating manga/metadata
- Whole code standards according to PyLint

### Deleted

- Packages
  - pillow
  - python-dotenv

###### Released On: 01 March 2023

---

## 1.6.0

### New

- Manga Metadata
  - Covers
  - Description
  - Author
  - Artist
  - Tags
- Update whole database metadata at once or one metadata at a time
- Issue template
  - Using yml instead of md
- [SVG icon](../src/static/manga_cover/default.svg)
- App arguments
  - `--version`
  - `--development`
  - `--logging`
- Development environment for devs
  - `app_runner.py --development`
- Logger
  -  Logs in the Apache Combined Log Format
- Settings to customise User Interface
- Configuration in `config.ini` file
- Rich progressbars and help messages
- New Font [Nunito](https://fonts.google.com/specimen/Nunito)

### Fixed/Updated

- Replace png image with svg icon
  - default.png -> default.svg
- Skipping check for update when no internet connection
- Updated database for additional metadata
  - Added
    - Author
    - Artist
  - Updated
    - Default image name in 'cover' column from default.png to default.svg
- Changed rendering file in sort function
  - sorted_manga.html -> table.html
- Updated import and export functions
- Showing MMDB version when running the app
- Updated navbar
- Updated ['About MMDB'](https://edwinrodger.github.io/MyMangaDataBase/) page
- Added colors to the messages
- Fixed bug where manga id and date was getting sent to URL after updating the manga
- Random placeholder text in search field everytime the page is loaded
- Change filename
  - home.html -> table.html
  - manga_id.html -> edit.html
  - create_manga.html -> create-manga.html
- Centered text in table
- New and clear routes for same function
- Updated links in readme.txt

### Deleted

- Old github issue files -
  - bug_report.md
  - feature_request.md
- sorted_manga.html
- Removed all "# type: ignore" (used to hide error less code warning messages)
- Removed .env file

###### Released On: 01 Feb 2023

---

## 1.5.0

### New

- Basic comments and docstrings in code
- Column for cover image (Though it only displays a default picture)
- Delete database route
- Linux support (Can be very buggy because it was tested using [WSL](https://learn.microsoft.com/en-us/windows/wsl/about))

### Fixed/Updated
- Better function names
- Changed MMDB export to .json file from .db file
- Drastically decrease the import time
- Default sorting is now alphabetical
- Updated packages
- Updated information messages
- Fixed a bug where score gets reset to zero every time you edit the manga
- Updated pipenv run commands

###### Released On: 01/01/2023

---

## 1.4.0

### New

- MyAnimeList import
- Warning messages when uploading wrong kind of backups
- Search Bar

### Fixed/Updated

- Updated edit manga page
- Changed link for about page
- External pages will now open in another tab
- Updated import messages

### Deleted

- Removed untested code
- About.html

---

## 1.3.0

### New

- Added repository and author's website
- Added `readme.txt` in zip file
- Added extra page for manga info
- New [Website](https://edwinrodger.github.com/MyMangaDataBase)
- [CODE_OF_CONDUCT.md](https://github.com/EdwinRodger/MyMangaDataBase/blob/main/.github/CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](https://github.com/EdwinRodger/MyMangaDataBase/blob/main/.github/CONTRIBUTING.md)
- [LICENSE](https://github.com/EdwinRodger/MyMangaDataBase/blob/main/LICENSE)
- [Issue Templates](https://github.com/EdwinRodger/MyMangaDataBase/tree/main/.github/ISSUE_TEMPLATE)

### Fixed/Updated

- Updated How to use and Contribution guide in `README.md`
- Updated software update checker
- Better choice handeling while asking for update

### Deleted

- requirements.txt
- MyMangaDataBase.sh
- MyMangaDataBase.bat

###### Released On: 12-11-2022

---

## 1.2.0

### New

- Added Import and Export for MMDB database

### Fixed/Updated

- Made a working sh file for MacOS and Linux system

###### Released On: 5-11-2022

---

## 1.1.0

### New

1. Added favicon
2. Using _Waitress_ module to host application

### Fixed/Updated

1. Decreased the time to start the app
2. Date showing when set to 01-01-0001
3. Did linting
4. Sorted Imports

### Help Wanted

1. If you can update `MyMangaDataBase.sh` file to run `app_runner.py` file, do share the code via pull request. It will help other UNIX users too
2. If there is any problem in `app_runner.py` file in MacOS or Linux, kindly fix that also as I am Windows user and don't know a thing about MacOS and Linux 😅

###### Released On: 31-10-2022

---

## 1.0.0

## First Release of MyMangaDataBase

###### Released On: 31-10-2022
