#!/usr/bin/env python
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


"""A simple performance test using POST requests with random valid URLS"""

import time
import random

import grequests

SERVER_URL = 'http://localhost:5000'
REQUESTS = 10000
CONCURRENT = 1000

# list of 1000 random urls scraped from http://www.uroulette.com/1000
with open('random_urls.txt') as f:
    urls = f.read().split()

beginning = time.time()

requests = [grequests.post(SERVER_URL, {'url': random.choice(urls)})
            for i in xrange(REQUESTS)]
responses = grequests.map(requests, size=CONCURRENT)

total = time.time() - beginning
print "Requests: " + str(REQUESTS)
print "Concurrent: " + str(CONCURRENT)
print "Average time per request: " + str(total/REQUESTS)
print "Total time: " + str(total)
