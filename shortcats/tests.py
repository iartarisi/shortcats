import unittest

import redis

from shortcats import shorten, expand
from shortcats.configs import rdb

TEST_URL = 'http://doesn.exist'
class ShortenTest(unittest.TestCase):

    def tearDown(self):
        rdb.flushdb()

    # shorten tests
    def test_shorten_already_exists(self):
        rdb.set('urls|'+TEST_URL, 'a1f')
        self.assertEqual(shorten(TEST_URL), 'a1f')

    def test_shorten_doesnt_exist_returns_valid(self):
        self.assertIsNone(rdb.get('urls|'+TEST_URL))
        self.assertEqual(shorten(TEST_URL), '1')

    def test_shorten_doesnt_exist_returns_next(self):
        rdb.set('url_counter', 51)
        self.assertEqual(shorten(TEST_URL), '1g')

    def test_shorten_doesnt_exist_creates_new(self):
        with self.assertRaises(KeyError):
            rdb['urls|'+TEST_URL]
        short = shorten(TEST_URL)
        self.assertEqual(rdb.get('urls|'+TEST_URL), '1')
        self.assertEqual(rdb.get('shorts|1'), TEST_URL)

    def test_shorten_doesnt_exist_creates_new_next(self):
        rdb.set('url_counter', 51)
        shorten(TEST_URL)
        self.assertEqual(rdb.get('urls|'+TEST_URL), '1g')
        self.assertEqual(rdb.get('shorts|1g'), TEST_URL)

    # expand tests
    def test_expand_doesnt_exist_returns_none(self):
        self.assertIsNone(expand('bogus'))

    def test_expands_exists(self):
        rdb.set('shorts|1g', TEST_URL)
        self.assertEqual(expand('1g'), TEST_URL)

    def test_expands_is_case_insensitive(self):
        rdb.set('shorts|2bogus', TEST_URL)
        self.assertEqual(expand('2BogUs'), TEST_URL)
