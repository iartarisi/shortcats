import json

import redis

try:
    with open('/home/dotcloud/environment.json') as f:
        conf = json.load(f)
except IOError:
    rdb = redis.Redis()
else:
    rdb = redis.Redis(host=conf['DOTCLOUD_DATA_REDIS_HOST'],
                  port=int(conf['DOTCLOUD_DATA_REDIS_PORT']),
                  password=conf['DOTCLOUD_DATA_REDIS_PASSWORD'],
                  )
