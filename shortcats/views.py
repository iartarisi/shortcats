import urllib2
from urlparse import urlparse

from flask import abort, redirect, render_template, request

from shortcats import app
from shortcats.backend import shorten, expand
from shortcats.utils import valid_url
from shortcats.configs import BASE_URL

OUR_HOSTNAME = urlparse(BASE_URL).hostname


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

    if OUR_HOSTNAME == urlparse(url).hostname:
        abort(400, "This is already a shortcats URL!")

    short = BASE_URL + shorten(url)

    return render_template("shortened.html", short=short, original=url)


@app.route("/<short>")
def expand_url(short):
    """Redirects the user to a URL which has already been shortened

    :short: a string which identifies an already shortened URL

    Returns 404 if the URL is not known to the application.

    """
    try:
        url = expand(short)
    except KeyError:
        abort(404)

    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if 'redirect error' in e.reason:
            abort(400, "The URL you were looking for contains a redirection "
                  "error, which makes it redirect infinitely.")
        abort(400, e)

    return redirect(url)
