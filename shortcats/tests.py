import unittest

import redis

from shortcats import shorten
from shortcats.configs import rdb

class ShortenTest(unittest.TestCase):

    def tearDown(self):
        rdb.flushdb()

    def test_shorten_already_exists(self):
        rdb.set('urls|http://existing.test', 'a1f')
        self.assertEqual(shorten('http://existing.test'), 'a1f')

    def test_shorten_doesnt_exist_returns_valid(self):
        self.assertIsNone(rdb.get('urls|http://doesnt.exist'))
        self.assertEqual(shorten('http://doesnt.exist'), '1')

    def test_shorten_doesnt_exist_returns_next(self):
        rdb.set('url_counter', 51)
        self.assertEqual(shorten('http://doesnt.exist'), '1g')

    def test_shorten_doesnt_exist_creates_new(self):
        with self.assertRaises(KeyError):
            rdb['urls|http://doesn.exist']
        shorten('http://doesn.exist')
        self.assertEqual(rdb.get('urls|http://doesn.exist'), '1')

    def test_shorten_doesnt_exist_creates_new_next(self):
        rdb.set('url_counter', 51)
        shorten('http://doesn.exist')
        self.assertEqual(rdb.get('urls|http://doesn.exist'), '1g')
