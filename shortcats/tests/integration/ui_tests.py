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

import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from shortcats.configs import BASE_URL, rdb

TEST_URL = 'http://example.com'


class UITest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        rdb.flushdb()
        self.driver.close()

    def test_index_has_shorten_form(self):
        self.driver.get(BASE_URL)
        form = self.driver.find_element_by_id('shorten')
        self.assertTrue(form)

    def test_shorten_url(self):
        self.driver.get(BASE_URL)
        url_field = self.driver.find_element_by_name('url')
        url_field.send_keys(TEST_URL)
        url_field.send_keys(Keys.RETURN)

        shortened = self.driver.find_element_by_id('shortened')
        self.assertEqual(shortened.tag_name, 'a')
        self.assertEqual(BASE_URL + '1', shortened.text)

        original = self.driver.find_element_by_id('original')
        self.assertEqual(original.tag_name, 'a')
        self.assertEqual(TEST_URL, original.text)

    def test_expand_url(self):
        rdb.set('shorts|myshorturl', TEST_URL)
        self.driver.get(BASE_URL + '/myshorturl')
        self.assertIn('IANA', self.driver.title)

    def test_expand_not_found(self):
        self.driver.get(BASE_URL + '/notfound')
        self.assertEqual(self.driver.title, '404 Not Found')

    def test_shorten_bad_url(self):
        self.driver.get(BASE_URL)
        url_field = self.driver.find_element_by_name('url')
        url_field.send_keys('not-a-valid-url')
        url_field.send_keys(Keys.RETURN)

        self.assertEqual(self.driver.title, '400 Bad Request')
        self.assertIn('malformed', self.driver.page_source)
