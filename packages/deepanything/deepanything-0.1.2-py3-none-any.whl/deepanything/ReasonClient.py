import openai
from openai.types.chat import chat_completion, chat_completion_chunk
from deepanything.Stream import Stream,AsyncStream
from deepanything import Utility


class ReasonClient:
    def __init__(self) -> None:
        pass

    def reason(
            self,
            messages:list[dict],
            model:str,
            stream = False,
            **kwargs
    ) -> Stream or chat_completion.ChatCompletion:
        if stream:
            return self.reason_stream(messages, model, **kwargs)

        return Utility.merge_chunk(
            self.reason_stream(messages, model, **kwargs),
            model
        )

    def reason_stream(self,
                      messages:list[dict],
                      model:str,
                      **kwargs
                      ) -> Stream:
        raise NotImplementedError

class AsyncReasonClient:
    def __init__(self) -> None:
        pass

    async def reason(
            self,
            messages:list[dict],
            model:str,
            stream = False,
            **kwargs
    ) -> AsyncStream or chat_completion.ChatCompletion:
        if stream:
            return await self.reason_stream(messages, model, **kwargs)

        return await Utility.async_merge_chunk(
            await self.reason_stream(messages, model, **kwargs),
            model
        )

    async def reason_stream(self,
                            messages:list[dict],
                            model:str,
                            **kwargs
                            ) -> AsyncStream:
        raise NotImplementedError

class DeepseekReasonClient(ReasonClient):
    client : openai.OpenAI

    def __init__(self,base_url:str,api_key:str,**kwargs) -> None:
        super().__init__()
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
            **kwargs
        )

    def reason_stream(self,
                      messages: list[dict],
                      model: str,
                      **kwargs
                      ) -> Stream:
        stream = self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
            **kwargs
        )

        def _iter():
            for chunk in stream:
                if chunk.choices[0].delta.reasoning_content is not None:
                    yield chunk
                else:
                    return


        return (Stream(_iter())
                .on_next(lambda it : it.__next__())
                .on_close(lambda _: stream.close()))

class AsyncDeepseekReasonClient(AsyncReasonClient):
    client : openai.AsyncOpenAI

    def __init__(self,base_url:str,api_key:str,**kwargs) -> None:
        super().__init__()
        self.client = openai.AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            **kwargs
        )

    async def reason_stream(self,
                            messages: list[dict],
                            model: str,
                            **kwargs
                            ) -> AsyncStream:
        stream = await self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
            **kwargs
        )

        async def _iter():
            async for chunk in stream:
                if chunk.choices[0].delta.reasoning_content is not None:
                    yield chunk
                else:
                    return


        return (AsyncStream(_iter())
                .on_next(lambda it : it.__anext__())
                .on_close(lambda _: stream.close()))


def _rebuild_chunk_for_openai(
        chunk:chat_completion_chunk.ChatCompletionChunk
) -> chat_completion_chunk.ChatCompletionChunk:
    chunk.choices[0].delta.reasoning_content = chunk.choices[0].delta.content
    chunk.choices[0].delta.content = None
    return chunk


class OpenaiReasonClient(ReasonClient):
    client : openai.OpenAI
    def __init__(
            self,
            base_url:str,
            api_key:str,
            **kwargs
    ) -> None:
        super().__init__()
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
            **kwargs
        )

    def reason_stream(self,
                      messages: list[dict],
                      model: str,
                      **kwargs
                      ) -> Stream:
        stream =  self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
            **kwargs
        )

        return Stream(stream).on_next(lambda it: _rebuild_chunk_for_openai(it.__next__())).on_close(lambda _: stream.close())

    def reason(
            self,
            messages:list[dict],
            model:str,
            stream = False,
            **kwargs
    ) -> Stream or chat_completion.ChatCompletion:
        if stream:
            return self.reason_stream(messages, model, **kwargs)
        completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=stream,
            **kwargs
        )

        completion.choices[0].message.reasoning_content = completion.choices[0].message.content
        completion.choices[0].message.content = None

        return completion

class AsyncOpenaiReasonClient(AsyncReasonClient):
    client : openai.AsyncOpenAI
    def __init__(self,base_url:str,api_key:str,**kwargs) -> None:
        super().__init__()
        self.client = openai.AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            **kwargs
        )

    async def reason_stream(self,
                            messages: list[dict],
                            model: str,
                            **kwargs
                            ) -> AsyncStream:

        stream =  await self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
            **kwargs
        )

        async def _next(it):
            return _rebuild_chunk_for_openai(await it.__anext__())

        return AsyncStream(stream).on_next(lambda it: _next(it)).on_close(lambda _: stream.close())

    async def reason(self,
                     messages: list[dict],
                     model: str,
                     stream = False,
                     **kwargs
                     ) -> AsyncStream or chat_completion.ChatCompletion:
        if stream:
            return await self.reason_stream(messages, model, **kwargs)

        completion = await self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs
        )

        completion.choices[0].message.reasoning_content = completion.choices[0].message.content
        completion.choices[0].message.content = None

        return completion