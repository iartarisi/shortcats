#!/usr/bin/env python

"""Fast gevent wsgi server"""

from gevent.wsgi import WSGIServer
from shortcats import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
