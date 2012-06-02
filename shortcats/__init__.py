#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, abort
app = Flask(__name__)

from shortcats.utils import base36_to_int, int_to_base36
from shortcats.configs import rdb

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<short>")
def expand_url(short):
    """Redirects the user to a URL which has already been shortened

    :short: a string which identifies an already shortened URL
 
    """
    try:
        return redirect(rdb['shorts|'+short])
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
        rdb.set('shorts|'+short, url)
        return short

def expand(short):
    """Expands a unique id into a URL from the database

    :short: a string which identifies an already shortened URL

    Returns a valid URL from the database or None if the id was not found.

    """
    return rdb.get('shorts|'+short.lower())

if __name__ == "__main__":
    app.run()
