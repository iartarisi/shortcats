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
