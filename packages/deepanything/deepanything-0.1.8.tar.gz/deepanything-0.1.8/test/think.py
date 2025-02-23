from deepanything.ReasonClient import DeepseekReasonClient
from deepanything.ResponseClient import OpenaiResponseClient
from deepanything.DeepAnythingClient import DeepAnythingClient

import asyncio

think_client = DeepseekReasonClient(
    base_url="https://api.siliconflow.cn/v1",
    api_key="sk-vyxfdewjjxgzctheaquyvelzcpixaapjkonktsnloqlyeelj"
)

response_client = OpenaiResponseClient(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-80d422aac1784a66bdb6e411ce91de53",
)

da_client = DeepAnythingClient(
    reason_client=think_client,
    response_client=response_client,
    reason_prompt="<Think>{}</Think>"
)
def main():
    # stream = da_client.chat_completion_stream(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "你好"
    #         }
    #     ],
    #     reason_model="Pro/deepseek-ai/DeepSeek-R1",
    #     response_model="qwen-max-latest",
    #     show_model="R1-qwen-max"
    # )
    #
    # for chunk in stream:
    #     print(chunk)
    res = da_client.chat_completion(
        messages=[
            {
                "role": "user",
                "content": "你好"
            }
        ],
        reason_model="Pro/deepseek-ai/DeepSeek-R1",
        response_model="qwen-max-latest",
        show_model="R1-qwen-max"
    )

    print(res)

main()