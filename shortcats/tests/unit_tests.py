import unittest

import redis

from shortcats import app
from shortcats.backend import shorten, expand
from shortcats.configs import rdb, BASE_URL

TEST_URL = 'http://doesn.exist'


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
        response = self.app.post('/', data=dict(url=BASE_URL+'not/us/?q=42'))
        self.assertEqual(response.status, '400 BAD REQUEST')

    # index
    def test_index_get_ok(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertIn('<form id="shorten" action="/" method="POST"',
                      response.data)