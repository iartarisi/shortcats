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
