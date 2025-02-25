<h1 align = "center">🔥公告🚀</h1>

---
<details markdown="1">
  <summary><b>🔥业务经营范围</b></summary>

- api服务（没有的找企微客服增加）
    - 提供主流大模型服务，gpt/claude/gemini/llama/国产大模型等等
    - 提供多模态模型服务，文件解析/图片解析/语音解析/视频解析等等
    - 提供垂类智能体服务，文件问答/联网问答/学术搜索等等
    - 提供语音克隆&语音合成服务，hailuo/fish/chattts等等
    - 提供embedding服务，bge/jina/openai等等
    - 提供图片生成服务，kling/flux/ideogram/recraft/虚拟换衣/换头等等
    - 提供视频生成服务，kling/cogviewx/hailuo/hunyuan/vidu/sora等等
    - 提供图片编辑服务，变清晰、去水印、抠图等等
    - 提供文档智能服务，ocr/pdf-to-markdown/url-to-markdown等等
    - 提供对象存储服务

- 账号服务（市面上有的都可以）
    - gpt-plus/claude-pro
    - api-key

- 个性化服务
    - 定制同款api聚合站点，一键对接货源
    - 定制企业智能体，类似gpt-4-all/kimi
    - 定制知识库智能问答（RAG）
    - 定制AI类网站/小程序等等
    - 承接数据标注/数据跑批任务
    - 承接大模型微调，定制化大模型（可端到端）
    - 承接其他项目，算法模型等等

</details>

<details markdown="1">
  <summary><b>大额对公，请联系客服</b></summary>
</details>

## 2025-02-20 新上模型
- jina-deepsearch 满血r1+搜索


---

<details markdown="1">
  <summary><b>历史更新</b></summary>

## 2025-01-04

- 增加模型配额 gemini-2.0-flash-exp、gemini-2.0-flash-thinking-exp-1219

## 2024-12-31

- 上线新模型
    - `glm-zero/glm-zero-preview`：GLM-Zero-Preview 专注于增强模型推理能力，擅长处理数理逻辑、代码和需要深度推理的复杂问题。同基座模型相比，GLM-Zero-Preview
      在不显著降低通用任务能力的情况下，在专家任务能力方面表现大幅提升。其在 AIME 2024、MATH500 和 LiveCodeBench 评测中，效果与
      OpenAI-o1-Preview 相当。
    - 兼容SparkAI客户端，文件问答&图片问答：baseurl改为`https://api.chatfire.cn/sparkai/v1`

## 2024-12-27

- 上线新模型
    - deepseek-v3
    - deepseek-r1：deepseek-v3的思考模型
    - deepseek-search：deepseek-v3的联网模型

## 2024-12-24

- 上线新模型
    - doubao-pro-256k：相比Doubao-pro-128k/240628，长文任务效果显著提升10%以上，要点提取、字数遵循、多轮对话上文记忆等能力大幅提升
    - [qvq-72b-preview](https://mp.weixin.qq.com/s/WzL7tbFUZOgE2IFMeHT-sQ)：Qwen开源视觉推理模型QVQ，更睿智地看世界！

- 增加gemini-2.0配额，支持多模型，默认分组可用
    - "gemini-2.0-flash"
    - "gemini-2.0-flash-exp"

## 2024-12-20

- 修复SunoV4无水印版本
    - [异步任务接口文档](https://api.chatfire.cn/docs/api-246593467)
- [增加视频解析模型](https://api.chatfire.cn/docs/api-246688638)
- 增加高并发mj-fast

## 2024-12-19

- 新增生图模型 SeedEdit（文生图&图生图/图片编辑）: 一句话编辑你的世界：字节跳动推出革命性图片编辑工具SeedEdit
    - [Chat模式接口文档](https://api.chatfire.cn/docs/api-214415540)
    - [Images接口文档](https://api.chatfire.cn/docs/api-246137616)
    - [异步任务接口文档](https://api.chatfire.cn/docs/api-246120232)
- 新增视觉模型
    - deepseek-ai/deepseek-vl2
    - doubao-vision-pro-32k
    - doubao-vision-lite-32k
- 新增视频模型 Sora
    - Chat模式：`sora-1:1-480p-5s`
    - 异步任务接口在路上

## 2024-12-13

- 新增模型 混元视频（支持高并发，非逆向可商用，限时特价1毛）[接口文档](https://api.chatfire.cn/docs/api-244309840)
  HunyuanVideo 是腾讯推出的开源视频生成基础模型，拥有超过 130
  亿参数，是目前最大的开源视频生成模型。该模型采用统一的图像和视频生成架构，集成了数据整理、图像-视频联合模型训练和高效基础设施等关键技术。模型使用多模态大语言模型作为文本编码器，通过
  3D VAE 进行空间-时间压缩，并提供提示词重写功能。根据专业人工评估结果，HunyuanVideo 在文本对齐、运动质量和视觉质量等方面的表现优于现有最先进的模型

## 2024-12-09

- 新增模型
    - meta-llama/Llama-3.3-70B-Instruct: Llama 3.3 是 Llama 系列最先进的多语言开源大型语言模型，以极低成本体验媲美 405B
      模型的性能。基于 Transformer
      结构，并通过监督微调（SFT）和人类反馈强化学习（RLHF）提升有用性和安全性。其指令调优版本专为多语言对话优化，在多项行业基准上表现优于众多开源和封闭聊天模型。知识截止日期为
      2023 年 12 月。
    - jimeng-v2.1：豆包画图，支持即梦超强图像生成能力，兼容chat/dalle-image调用方式。
    - 海螺最新的I2V-01-live图生视频模型：特别针对二次元图生视频效果，进行了优化，动作流畅又生动，让2D二次元角色像复活一样。

## 2024-12-06

- 新增模型
    - o1-plus: （官网 plus 版本 `逆向工程`，有思考过程显示）o1 是OpenAI针对复杂任务的新推理模型，该任务需要广泛的常识。该模型具有
      200k 上下文，目前全球最强模型，支持图片识别
    - o1-pro: （官网 200刀 plus 版本 `逆向工程`，有思考过程显示）o1-pro 是OpenAI针对复杂任务的新推理模型，该任务需要广泛的常识。该模型具有
      200k 上下文，目前全球最强模型，支持图片识别

## 2024-12-05

- 新增模型gpt-4-plus/gpt-4o-plus按倍率计算
  > OpenAI-plus会员 逆向工程

## 2024-11-29

- 新增推理模型
    - Qwen/QwQ-32B-Preview
      > 强大的数学问题解决能力，在AIME、MATH-500数学评测上，超过了OpenAI o1-preview优秀的编码能力，LiveCodeBench接近OpenAI
      o1-preview

## 2024-11-25

- 新增虚拟换衣接口
    - [可灵官方api格式](https://api.chatfire.cn/docs/api-237182295) 0.8/次
    - [老接口格式](https://api.chatfire.cn/docs/api-226983436) 0.1/次

</details>
