from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/500.html"), 500

@errors.route("/errors/<int:error>")
def err(error):
    if error == 404:
        return render_template("errors/404.html")
    if error == 500:
        return render_template("errors/500.html")