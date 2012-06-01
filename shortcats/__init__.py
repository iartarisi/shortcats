#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask
app = Flask(__name__)

from shortcats.utils import base36_to_int, int_to_base36
from shortcats.configs import rdb

@app.route("/")
def hello():
    return "Hello World!"

def shorten(url):
    """Shortens a given url, returning the unique id of that url"""
    existing_url = rdb.get('urls|' + url)

    if existing_url:
        return existing_url
    else:
        counter = rdb.incr('url_counter')
        link_id = int_to_base36(counter)
        rdb.set('urls|' + url, link_id)
        return link_id

if __name__ == "__main__":
    app.run()
