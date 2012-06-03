# -*- coding: utf-8 -*-
# Copyright (c) 2012 Ionuț Arțăriși <ionut@artarisi.eu>
# This file is part of Shortcats.

# Shortcats is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Shortcats is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Shortcats.  If not, see <http://www.gnu.org/licenses/>.

from shortcats.utils import int_to_base36
from shortcats.configs import rdb


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
