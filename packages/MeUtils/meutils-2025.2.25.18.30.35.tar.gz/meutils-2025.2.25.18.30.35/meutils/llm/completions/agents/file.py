#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2025/1/3 15:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 支持文档、图片、音频、视频问答
"""单一智能体
任意模型支持文档、图片、音频、视频问答
api形式
- /agents/v1
- /v1 前缀区分 agents-{model}【底层调用 /agents/v1】

todo: 记录上下文日志
"""

from meutils.pipe import *
from meutils.parsers.file_parsers import file_extract

from meutils.llm.clients import AsyncOpenAI
from meutils.llm.openai_utils import to_openai_params

from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, ChatCompletionRequest, CompletionUsage


class Completions(object):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def create(self, request: ChatCompletionRequest):
        """[{'role': 'user', 'content': 'hi'}]
        {"type": "file_url", "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}}"""

        if urls := parse_url(str(request.messages)):
            logger.debug(urls)

            file_reponse = await file_extract(urls[-1])
            if file_reponse:  # 仅关注最后一个
                request.system_messages.append({
                    "role": "system",
                    "content": json.dumps(file_reponse, ensure_ascii=False),
                })

            request.messages = request.system_messages + request.messages

        logger.debug(request)

        data = to_openai_params(request)
        return await AsyncOpenAI(api_key=self.api_key).chat.completions.create(**data)


# data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\n\n
if __name__ == '__main__':
    c = Completions()

    request = ChatCompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="claude-3-5-sonnet-20241022",
        model="gpt-4o-mini",

        messages=[
            {
                'role': 'system',
                'content': '你是一个文件问答助手'
            },
            # {
            #     'role': 'user',
            #     # 'content': {
            #     #     "type": "file_url",
            #     #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #     # },
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "这个文件讲了什么？"
            #         },
            #         # 多轮的时候要剔除
            #         {
            #             "type": "file_url",
            #             "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #         }
            #     ]
            # },

            {
                'role': 'user',
                # 'content': {
                #     "type": "file_url",
                #     "file_url": {"url": "https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf", "detai": "auto"}
                # },
                # 'content': "https://oss.ffire.cc/files/%E6%8B%9B%E6%A0%87%E6%96%87%E4%BB%B6%E5%A4%87%E6%A1%88%E8%A1%A8%EF%BC%88%E7%AC%AC%E4%BA%8C%E6%AC%A1%EF%BC%89.pdf 这个文件讲了什么？",
                # 'content': "https://translate.google.com/?sl=zh-CN&tl=en&text=%E6%8F%90%E4%BE%9B%E6%96%B9&op=tr1anslate 这个文件讲了什么？",

                # "content": "总结下 https://oss.ffire.cc/files/百炼系列手机产品介绍.docx"
                # "content": "https://mj101-1317487292.cos.ap-shanghai.myqcloud.com/ai/test.pdf\n\n总结下"

                "content": "https://admin.ilovechatgpt.top/file/lunIMYAIzhinengzhushouduishenghuodocx_14905733.docx 总结"

            },

            # {'role': 'assistant', 'content': "好的"},
            # {
            #     'role': 'user',
            #     # 'content': {
            #     #     "type": "file_url",
            #     #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #     # },
            #     'content': [
            #         {
            #             "type": "text",
            #             "text": "错了 继续回答"
            #         },
            #         # {
            #         #     "type": "file_url",
            #         #     "file_url": {"url": "https://oss.ffire.cc/files/招标文件备案表（第二次）.pdf", "detai": "auto"}
            #         # }
            #     ]
            # }
        ]

    )

    arun(c.create(request))
