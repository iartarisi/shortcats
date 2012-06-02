from flask import abort, redirect, render_template, request

from shortcats import app
from shortcats.backend import shorten, expand
from shortcats.utils import valid_url
from shortcats.configs import BASE_URL


@app.route("/", methods=['GET'])
def index():
    """Show our front page"""
    return render_template("index.html")


@app.route("/", methods=['POST'])
def shorten_url():
    """Shortens a URL, returning a URL which will redirect to :url:

    :url: a valid URL which should be shortened

    """
    try:
        url = request.form['url']
    except KeyError:
        abort(400, "The required 'url' form value argument was not provided.")

    if not valid_url(url):
        abort(400, "The URL you have entered is malformed!")

    short = BASE_URL + shorten(url)

    return render_template("shortened.html", short=short, original=url)


@app.route("/<short>")
def expand_url(short):
    """Redirects the user to a URL which has already been shortened

    :short: a string which identifies an already shortened URL

    Returns 404 if the URL is not known to the application.

    """
    try:
        return redirect(expand(short))
    except KeyError:
        abort(404)
