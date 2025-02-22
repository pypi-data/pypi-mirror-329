from deepanything.ReasonClient import AsyncDeepseekReasonClient
from deepanything.ResponseClient import AsyncOpenaiResponseClient
from deepanything.DeepAnythingClient import AsyncDeepAnythingClient

import asyncio

think_client = AsyncDeepseekReasonClient(
    base_url="https://api.siliconflow.cn/v1",
    api_key="sk-vyxfdewjjxgzctheaquyvelzcpixaapjkonktsnloqlyeelj"
)

response_client = AsyncOpenaiResponseClient(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-80d422aac1784a66bdb6e411ce91de53",
)

da_client = AsyncDeepAnythingClient(
    think_client=think_client,
    response_client=response_client,
    think_prompt="<Think>{}</Think>"
)
async def main():
    stream = await da_client.chat_completion_stream(
        messages=[
            {
                "role": "user",
                "content": "你好"
            }
        ],
        think_model="Pro/deepseek-ai/DeepSeek-R1",
        response_model="qwen-max-latest",
        show_model="R1-qwen-max"
    )

    async for chunk in stream:
        print(chunk)

asyncio.run(main())