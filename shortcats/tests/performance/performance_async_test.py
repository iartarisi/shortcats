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


"""A simple performance test using POST requests with random URLS"""

import time
import random

import grequests

SERVER_URL = 'http://localhost:5000'
REQUESTS = 10001
BROKEN = 5000  # number of invalid urls (the rest will be valid)
CONCURRENT = 1000

# list of 1000 random urls scraped from http://www.uroulette.com/1000
with open('random_urls.txt') as f:
    urls = f.read().split()

random_urls = [random.choice(urls) for i in xrange(REQUESTS)]
# break a number of urls (indicated by BROKEN) randomly by shuffling
# their letters around
for i in xrange(BROKEN):
    x = random.randint(1, REQUESTS)
    url_letters = [l for l in random_urls[x]]
    random.shuffle(url_letters)
    random_urls[x] = ''.join(url_letters)

requests = [grequests.post(SERVER_URL, {'url': url}) for url in random_urls]

beginning = time.time()
responses = grequests.map(requests, size=CONCURRENT)
total = time.time() - beginning

print "Requests: " + str(REQUESTS)
print "Concurrent: " + str(CONCURRENT)
print "Average time per request: " + str(total/REQUESTS)
print "Total time: " + str(total)
