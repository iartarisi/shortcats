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
from multiprocessing import Process
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

from shortcats import app
from shortcats.configs import rdb

TEST_URL = 'http://localhost:8000/l33t'
TEST_PORT = 8000


def redirection_server(environ, start_response):
    setup_testing_defaults(environ)

    headers = [('Content-Type', 'text/plain'),
               ('Location', TEST_URL)]
    status = '301 Moved Permanently'

    start_response(status, headers)

    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    return ret


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        httpd = make_server('', TEST_PORT, redirection_server)
        self.server = Process(target=httpd.serve_forever, args=())
        self.server.start()

    def tearDown(self):
        self.server.terminate()

    def test_infinite_redirects_not_ok(self):
        rdb['shorts|bad_redirect'] = TEST_URL
        res = self.app.get('/bad_redirect')
        self.assertEqual(res.status, '400 BAD REQUEST')
        self.assertIn('redirection error', res.data)
