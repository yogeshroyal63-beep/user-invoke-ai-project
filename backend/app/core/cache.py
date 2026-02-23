# app/core/cache.py

import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def cache_get(key):
    val = r.get(key)
    if val:
        return json.loads(val)
    return None


def cache_set(key, value, ttl=3600):
    r.setex(key, ttl, json.dumps(value))