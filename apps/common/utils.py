import redis

redis_client = redis.Redis(host="redis", port=6379, db=0)

def rate_limit(key, limit=10, window=60):
    current = redis_client.get(key)
    if current and int(current) >= limit:
        return False
    pipe = redis_client.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, window)
    pipe.execute()
    return True