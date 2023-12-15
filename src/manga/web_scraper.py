import requests
from bs4 import BeautifulSoup

import src.manga.utils as manga_utils


# Collects metadata of manga from ManagUpdates which contains description, genres etc.
def manga_metadata(url, title):
    # Making a GET request
    response = requests.get(url, timeout=30)
    # Parsing the HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Checks for divs which contains metadata
    # I have divided the page into two sides - left[0] and right[1]
    side = soup.find_all("div", class_="col-6 p-2 text")
    # Checks left side content for description. As description is first in list
    # so no extra variable is used
    manga_desc = side[0].find(class_="sContent")
    # Check for right side content which contais data of image, genre, author and artist
    content = side[1].find_all(class_="sContent")
    # Checks all image url on the webpage. It is used for cover of manga.
    images = side[1].find_all(class_="img-fluid")

    # Getting Manga Description and removing duplicate and extra stuff
    manga_description = manga_desc.text.strip()
    if "More..." in manga_description:
        manga_description = manga_description.split("More...\n\n\n")
        manga_description = " ".join(manga_description[1:]).replace("Less...", "")
    # After collecting the image on right side (cover image), we send it to get downloaded.
    try:
        manga_cover = manga_utils.online_image_downloader(
            images[0].get("src").strip(), title
        )
    except IndexError:
        print("Image couldn't be retrieved: ", title)
        manga_cover = "default-manga.svg"
    # Index 1 on content consists of genre
    # .split is to remove last suggestion from the genre i.e. "Search for series of same genre(s)"
    manga_genre = content[1].text.split("\xa0")
    manga_genre = ", ".join(manga_genre[:-1])
    # Index 5 on content consists of author
    manga_author = content[5].text.replace("[Add]", "")
    # Index 6 on content consists of Artist
    manga_artist = content[6].text.replace("[Add]", "")
    print("Metadata successfully updated: ", title)
    return [
        str(manga_artist),
        str(manga_author),
        str(manga_cover),
        str(manga_description),
        str(manga_genre),
    ]


# Searches MangaUpdates for manga title and sends the first recommendation to manga_metadata
# function
def manga_search(title):
    # Default search URL with manga title as seach query and Making a GET request
    response = requests.get(
        f"https://www.mangaupdates.com/search.html?search={title}", timeout=30
    )
    # Parsing the HTML
    soup = BeautifulSoup(response.content, "html.parser")
    # Getting div class of "Series Info" -> "Title" -> First Recommendation
    series = soup.find_all("div", class_="col-6 py-1 py-md-0 text")
    # Getting <a> tag from first recommendation div
    try:
        atag = series[0].find_all("a")
    except IndexError:
        print("Manga not found: ", title)
        return [
            None,
            None,
            "default-manga.svg",
            "Manga not found on MangaUpdates",
            None,
        ]
    # Getting URL from <a> tag's href
    url = atag[0].get("href")
    # Calling manga_metadata function to return manga metadata
    return manga_metadata(url, title)
