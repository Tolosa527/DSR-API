import redis
from digital import settings


def get_redis_client():

    """
    Returns a redis client

    usage:

        client = get_redis_client()
    """
    client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return client
