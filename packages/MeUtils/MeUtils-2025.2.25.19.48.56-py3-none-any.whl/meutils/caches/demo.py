import asyncio

from collections import namedtuple

from aiocache import cached, Cache, RedisCache
from aiocache.serializers import PickleSerializer
# With this we can store python objects in backends like Redis!

Result = namedtuple('Result', "content, status")


@cached(
    cache=RedisCache(), key="key", serializer=PickleSerializer(), port=6379, namespace="main")
async def cached_call():
    print("Sleeping for three seconds zzzz.....")
    await asyncio.sleep(3)
    return Result("content", 200)


async def run():
    await cached_call()
    await cached_call()
    await cached_call()
    cache = Cache(Cache.REDIS, endpoint="127.0.0.1", port=6379, namespace="main")
    await cache.delete("key")

if __name__ == "__main__":
    asyncio.run(run())