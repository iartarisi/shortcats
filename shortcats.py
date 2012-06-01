#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask
app = Flask(__name__)

from shortcats.utils import base36_to_int
from shortcats.configs import rdb

@app.route("/")
def hello():
    return "Hello World!"

def shorten(url):
    """Shortens a given url"""
    rdb.incr('url_counter')
    raise Exception
    

if __name__ == "__main__":
    app.run()
