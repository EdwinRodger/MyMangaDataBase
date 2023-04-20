import json
import datetime
from src.models import Manga

def log_chapter(manga_title:str, count:int):
    # Get the current date and format it as a string
    current_date = datetime.date.today().strftime("%Y-%m-%d")

    # Load the existing data from the JSON file
    with open("json/chapter-log.json", "r") as f:
        data = json.load(f)
        print(data)
    
    # Initialising previous_count
    previous_count = 0
    # Get previous count if any
    if current_date in data:
        if manga_title in data[current_date]:
            previous_count = data[current_date][manga_title]

    # Update the data with the new information
    if current_date in data:
        data[current_date][manga_title] = previous_count + count
    else:
        data[current_date] = {manga_title: previous_count + count}

    # Save the updated data to the JSON file
    with open("json/chapter-log.json", "w") as f:
        json.dump(data, f, indent=4)
