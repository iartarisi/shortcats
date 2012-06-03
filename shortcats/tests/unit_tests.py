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

import urllib2
import unittest


import redis

from shortcats import app
from shortcats.backend import shorten, expand
from shortcats.configs import rdb, BASE_URL

TEST_URL = 'http://doesn.exist'

# mock urllib2 for views which check the validity of an URL
urllib2.urlopen = lambda url: True


class ShortenTest(unittest.TestCase):

    def tearDown(self):
        rdb.flushdb()

    # shorten tests
    def test_shorten_already_exists(self):
        rdb.set('urls|' + TEST_URL, 'a1f')
        self.assertEqual(shorten(TEST_URL), 'a1f')

    def test_shorten_doesnt_exist_returns_valid(self):
        self.assertIsNone(rdb.get('urls|' + TEST_URL))
        self.assertEqual(shorten(TEST_URL), '1')

    def test_shorten_doesnt_exist_returns_next(self):
        rdb.set('url_counter', 51)
        self.assertEqual(shorten(TEST_URL), '1g')

    def test_shorten_doesnt_exist_creates_new(self):
        with self.assertRaises(KeyError):
            rdb['urls|' + TEST_URL]
        shorten(TEST_URL)
        self.assertEqual(rdb.get('urls|' + TEST_URL), '1')
        self.assertEqual(rdb.get('shorts|1'), TEST_URL)

    def test_shorten_doesnt_exist_creates_new_next(self):
        rdb.set('url_counter', 51)
        shorten(TEST_URL)
        self.assertEqual(rdb.get('urls|' + TEST_URL), '1g')
        self.assertEqual(rdb.get('shorts|1g'), TEST_URL)

    # expand tests
    def test_expand_doesnt_exist_returns_none(self):
        self.assertRaises(KeyError, expand, 'bogus')

    def test_expands_exists(self):
        rdb.set('shorts|1g', TEST_URL)
        self.assertEqual(expand('1g'), TEST_URL)

    def test_expands_is_case_insensitive(self):
        rdb.set('shorts|2bogus', TEST_URL)
        self.assertEqual(expand('2BogUs'), TEST_URL)


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        rdb.flushdb()

    # expand_url
    def test_expand_url_not_found(self):
        response = self.app.get('/notfound')
        self.assertEqual(response.status, '404 NOT FOUND')

    def test_expand_url_redirects(self):
        rdb.set('shorts|asdf', TEST_URL)
        response = self.app.get('/asdf')
        self.assertEqual(response.status, '302 FOUND')

    def test_expand_url_404_passes_through(self):
        rdb.set('shorts|404g', 'http://google.com/404')
        response = self.app.get('/404g')
        self.assertEqual(response.status, '302 FOUND')
        self.assertEqual(response.location, 'http://google.com/404')

    def test_expand_url_inexistent_passes_through(self):
        rdb.set('shorts|bad', 'http://bad.badbad')
        response = self.app.get('/bad')
        self.assertEqual(response.status, '302 FOUND')
        self.assertEqual(response.location, 'http://bad.badbad')
        
    # shorten_url
    def test_shorten_url(self):
        response = self.app.post('/', data=dict(url=TEST_URL))
        self.assertEqual(response.status, '200 OK')
        self.assertIn('<a id="original" href="%(original)s">%(original)s</a>'
                      % dict(original=TEST_URL),
                      response.data)
        self.assertIn('<a id="shortened" href="%(short)s">%(short)s</a>'
                      % dict(short=BASE_URL + '1'),
                      response.data)

    def test_shorten_url_no_url_arg(self):
        response = self.app.post('/', data=dict())
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_shorten_url_invalid_url(self):
        response = self.app.post('/', data=dict(url='http://bogus!'))
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_shorten_url_doesnt_redirect_back_to_us(self):
        response = self.app.post('/', data=dict(url=BASE_URL + 'not/us/?q=42'))
        self.assertEqual(response.status, '400 BAD REQUEST')

    # index
    def test_index_get_ok(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertIn('<form id="shorten" action="/" method="POST"',
                      response.data)
