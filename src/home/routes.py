from flask import Blueprint, render_template, request

from src.home.utils import (
    anime_overview_data,
    check_for_update,
    manga_overview_data,
    mmdb_promotion,
)

home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
def homepage():
    manga_data = manga_overview_data()
    anime_data = anime_overview_data()
    show_update_modal = check_for_update()
    return render_template(
        "home.html",
        title="Home",
        current_section="Home",
        manga_data=manga_data,
        anime_data=anime_data,
        show_update_modal=show_update_modal,
    )


@home.route("/more")
def more():
    return render_template("more.html", title="More", current_section="More")


@home.route("/credits")
def credits():
    return render_template("credits.html", title="Credits", current_section="More")


@home.before_request
def before_request():
    endpoint = request.endpoint
    action = {
        "home.more": more,
        "home.credits": credits,
    }.get(endpoint, more)

    mmdb_promotion(action)()
