#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : qwen
# @Time         : 2025/1/17 16:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
"""
 File "/usr/local/lib/python3.10/site-packages/meutils/llm/completions/qwenllm.py", line 47, in create
    yield response.choices[0].message.content
AttributeError: 'str' object has no attribute 'choices'

"""

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.llm.openai_utils import to_openai_params

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=PP1PGr"

base_url = "https://chat.qwenlm.ai/api"

from fake_useragent import UserAgent

ua = UserAgent()


async def create(request: ChatCompletionRequest):
    token = await get_next_token_for_polling(feishu_url=FEISHU_URL)

    client = AsyncOpenAI(
        base_url=base_url, api_key=token,
        default_headers={'User-Agent': ua.random}
    )

    # qwen结构
    if any(i in request.model.lower() for i in ("search",)):
        request.model = "qwen-plus-latest"
        request.messages[-1]['chat_type'] = "search"

    if any(i in request.model.lower() for i in ("qwq", "think")):
        request.model = "qwen-plus-latest"
        request.messages[-1]['feature_config'] = {"thinking_enabled": True}

    data = to_openai_params(request)

    if request.stream:
        _chunk = ""
        async for chunk in await client.chat.completions.create(**data):
            chunk = chunk.choices[0].delta.content or ""
            yield chunk.removeprefix(_chunk)
            _chunk = chunk

    else:
        response = await client.chat.completions.create(**data)
        if isinstance(response, str):
            logger.error(response)
        else:
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
        # model="qwen-max-latest",
        model="qwen-max-latest-search",

        # model="qwen-plus-latest",

        messages=[
            {
                'role': 'user',
                # 'content': '今天南京天气',
                # 'content': '总结下',

                # "chat_type": "search",

                "content": [
                    {
                        "type": "text",
                        "text": "总结下",
                        "chat_type": "t2t",
                        "feature_config": {
                            "thinking_enabled": False
                        }
                    },
                    {
                        "type": "file",
                        "file": "2d677df1-45b2-4f30-829f-0d42b2b07136"
                    }
                ]

            },

        ],
        stream=True,

    )
    arun(create(request))
