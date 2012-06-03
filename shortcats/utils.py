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

import re


def int_to_base36(i):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    factor = 0
    # Find starting factor
    while True:
        factor += 1
        if i < 36 ** factor:
            factor -= 1
            break
    base36 = []
    # Construct base36 representation
    while factor >= 0:
        j = 36 ** factor
        base36.append(digits[i / j])
        i = i % j
        factor -= 1
    return ''.join(base36)


def valid_url(url):
    """Returns True if the :url: string is a valid URL, False otherwise"""
    # thank you django.core.validators
    regex = re.compile(
        r'^(?:http|ftp)s?://'                             # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'            # domain...
        r'localhost|'                                     # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'            # ...or ip
        r'(?::\d+)?'                                      # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.match(url):
        return True
    else:
        return False
