import os
from urllib.parse import urlparse

import redis

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

url = urlparse(redis_url)

redis_client = redis.StrictRedis(
    host=url.hostname or 'localhost',
    port=url.port or 6379,
    db=int(url.path[1:]) if url.path else 0,
    decode_responses=True
)