from flask import Blueprint, render_template
import requests
import random

errors = Blueprint("errors", __name__)


# List of reactions for 404 error
reactions_404 = ['facepalm', 'mad', 'smack']
# List of reactions for 500 error
reactions_500 = ['nervous', 'sorry', 'surprised', 'sweat', 'confused']
# Base URL for the API
api_base_url = 'https://api.otakugifs.xyz/gif'

# Function to retrieve the GIF URL for a given reaction
def get_gif_url(reaction):
    url = f"{api_base_url}?reaction={reaction}&format=WebP"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        gif_url = data["url"]
        return gif_url
    return None

# Function to get the GIF URL based on the error code and a list of reactions
def gif_url(code):
    if code == 404:
        reactions = reactions_404
    else:
        reactions = reactions_500
    # Randomly select a reaction from the given list
    reaction = random.choice(reactions)
    # Get the GIF URL for the selected reaction
    gif_url = get_gif_url(reaction)
    if gif_url is not None:
        return gif_url
    return None



@errors.app_errorhandler(404)
def error_404(error):
    url = gif_url(404)
    return render_template("errors/404.html", url = url), 404


@errors.app_errorhandler(500)
def error_500(error):
    url = gif_url(500)
    return render_template("errors/500.html", url = url), 500


@errors.route("/errors/<int:error>")
def err(error):
    if error == 404:
        url = gif_url(404)
        return render_template("errors/404.html", url = url)
    if error == 500:
        url = gif_url(500)
        return render_template("errors/500.html", url = url)
