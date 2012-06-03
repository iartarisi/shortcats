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

import json

import redis

try:
    with open('/home/dotcloud/environment.json') as f:
        conf = json.load(f)
except IOError:
    rdb = redis.Redis()
    BASE_URL = 'http://localhost:5000/'
else:
    # dotcloud
    BASE_URL = conf['DOTCLOUD_WWW_HTTP_URL']
    rdb = redis.Redis(host=conf['DOTCLOUD_DATA_REDIS_HOST'],
                  port=int(conf['DOTCLOUD_DATA_REDIS_PORT']),
                  password=conf['DOTCLOUD_DATA_REDIS_PASSWORD'],
                  )
