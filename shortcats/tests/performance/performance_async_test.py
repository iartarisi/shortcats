#!/usr/bin/env python

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
