#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : acache
# @Time         : 2025/1/14 09:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from meutils.db.redis_db import async_pool

from aiocache import cached

from aiocache import cached, Cache, RedisCache, caches
from aiocache import multi_cached

logger.debug(async_pool.connection_kwargs)
def rcache(**kwargs): # todo
    # if REDIS_URL := os.getenv("REDIS_URL"):
    # endpoint = "127.0.0.1",
    # port = 6379,
    # db = 0,
    # password = None,

    return cached(
        cache=RedisCache,
        # endpoint=REDIS_URL,
        # connection_pool_kwargs=1,
        **async_pool.connection_kwargs,
        **kwargs
    )



@cached(ttl=60)
@cached(ttl=60)
async def cached_fc(user_id, **kwargs):
    logger.debug(user_id)
    return False





@rcache(ttl=3)
async def redis_fc(user_id, **kwargs):
    logger.debug(user_id)
    return False


# @multi_cached(ttl=60) # 多key缓存
# async def complex_function(user_id, **kwargs):
#     logger.debug(user_id)
#     return False


# Cache.MEMORY

# Cache.REDIS
# mcache = cached(ttl=60, cache=Cache.REDIS)(cached)
# from aiocache import Cache
#
# Cache(Cache.REDIS)
#
# rcache = Cache.from_url("redis://:chatfirechatfire@110.42.51.201:6379/11")
# print(rcache)


# @cached(ttl=60)
# @cached(ttl=15, cache=rcache)
# async def complex_function(user_id, **kwargs):
#     logger.debug(user_id)
#     return False
#

class A(BaseModel):
    a: Any = 111


import asyncio
from aiocache import cached
from aiocache.backends.redis import RedisCache
from aiocache.serializers import PickleSerializer


# 使用 @cached 装饰器缓存函数结果
@cached(cache=RedisCache, endpoint="127.0.0.1", port=6379, namespace="main",
        # serializer=PickleSerializer(),
        key="my_key", ttl=60)
async def expensive_operation():
    print("Performing expensive operation...")
    await asyncio.sleep(2)  # 模拟耗时操作
    return {"result": "data"}



if __name__ == '__main__':

    async def main():
        for i in range(10):
            logger.debug(i)

            await redis_fc(A())
            await asyncio.sleep(1)


    arun(main())
