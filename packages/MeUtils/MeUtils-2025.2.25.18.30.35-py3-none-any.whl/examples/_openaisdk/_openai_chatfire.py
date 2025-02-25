#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError


client = OpenAI(
    api_key="你的 https://api.chatfire.cn/token",
    base_url="https://api.chatfire.cn/v1"
)


completion = client.chat.completions.create(
    model="glm-4-flash",
    # model="xxxxxxxxxxxxx",
    messages=[
        {"role": "system", "content": '你是个内容审核助手'},

        {"role": "user", "content": message}
    ],
    # top_p=0.7,
    top_p=None,
    temperature=None,
    stream=True,
    max_tokens=1000
)


for chunk in completion:
    # print(bjson(chunk))
    print(chunk.choices[0].delta.content, end="")

