#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, redirect, render_template, request
app = Flask(__name__)

from shortcats.utils import int_to_base36, valid_url
from shortcats.configs import rdb, BASE_URL


@app.route("/")
def index():
    """Show our front page"""
    return render_template("index.html")


@app.route("/shorten", methods=['POST'])
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


def shorten(url):
    """Shortens a given URL, returning the unique id of that URL

    :url: a valid URL string

    The URL will be recorded in the database if it does not already exist.

    Returns a string id composed of lowercase alphanumeric characters

    """
    existing_url = rdb.get('urls|' + url)

    if existing_url:
        return existing_url
    else:
        counter = rdb.incr('url_counter')
        short = int_to_base36(counter)
        rdb.set('urls|' + url, short)
        rdb.set('shorts|' + short, url)
        return short


def expand(short):
    """Expands a unique id into a URL from the database

    :short: a string which identifies an already shortened URL

    Returns a valid URL from the database. Raises a KeyError if the id
    was not found.

    """
    return rdb['shorts|' + short.lower()]

if __name__ == "__main__":
    app.run(debug=True)
