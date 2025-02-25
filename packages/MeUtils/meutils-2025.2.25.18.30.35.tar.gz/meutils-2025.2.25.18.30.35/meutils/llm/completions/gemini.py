#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : gemini
# @Time         : 2025/2/14 17:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.llm.openai_utils import to_openai_params
from meutils.llm.clients import chatfire_client

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage

"""
image => file

      "type": "image_url",
      "image_url": {
          

"""


async def create(request: ChatCompletionRequest):
    data = to_openai_params(request)

    if request.stream:
        _chunk = ""
        async for chunk in await chatfire_client.chat.completions.create(**data):
            chunk = chunk.choices[0].delta.content or ""
            yield chunk.removeprefix(_chunk)
            _chunk = chunk

    else:
        response = await client.chat.completions.create(**data)
        # logger.info(response)
        yield response.choices[0].message.content


if __name__ == '__main__':
    # [
    #     "qwen-plus-latest",
    #     "qvq-72b-preview",
    #     "qwq-32b-preview",
    #     "qwen2.5-coder-32b-instruct",
    #     "qwen-vl-max-latest",
    #     "qwen-turbo-latest",
    #     "qwen2.5-72b-instruct",
    #     "qwen2.5-32b-instruct"
    # ]
    request = ChatCompletionRequest(
        # model="qwen-turbo-2024-11-01",
        model="qwen-max-latest",
        # model="qwen-plus-latest",

        messages=[
            {
                'role': 'user',
                'content': 'hi'
            },

        ],
        stream=False,
    )
    arun(create(request))
