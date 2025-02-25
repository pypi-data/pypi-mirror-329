#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat
# @Time         : 2024/8/19 14:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
from openai import Client, AsyncClient, AsyncStream, APIStatusError

from meutils.pipe import *

OpenAI = lru_cache(Client)
AsyncOpenAI = lru_cache(AsyncClient)

chatfire_client = AsyncOpenAI()

moonshot_client = AsyncOpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url=os.getenv("MOONSHOT_BASE_URL")
)
zhipuai_client = AsyncOpenAI(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    base_url=os.getenv("ZHIPUAI_BASE_URL")
)

qwen_client = AsyncOpenAI(
    base_url="https://all.chatfire.cn/qwen/v1",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMxMGNiZGFmLTM3NTQtNDYxYy1hM2ZmLTllYzgwMDUzMjljOSIsImV4cCI6MTc0MzAzNTk4OH0.GVAoSFtK94a9CgxqHCEnxzAnRi7gafIvYyH9mIJUh4s"
)

# zhipuai_client = OpenAI(
#     api_key=os.getenv("ZHIPUAI_API_KEY"),
#     base_url=os.getenv("ZHIPUAI_BASE_URL")
# )

if __name__ == '__main__':
    from meutils.pipe import *

    # OpenAI().chat.completions.create(messages=[{"role": "user", "content": "hi"}], model='glm-4-flash')

    # arun(zhipuai_client.chat.completions.create(messages=[{"role": "user", "content": "hi"}], model='glm-4-flash'))

    # web-search-pro
    # s = zhipuai_client.chat.completions.create(
    #     messages=[{"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}],
    #     model='web-search-pro',
    #     stream=True
    # )
    #
    # r = arun(zhipuai_client.chat.completions.create(
    #     messages=[{"role": "user", "content": "《哪吒之魔童闹海》现在的票房是多少"}],
    #     model='web-search-pro',
    #     stream=True
    # )
    # )

    # r.model_dump_json()
