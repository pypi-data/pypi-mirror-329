from openai import OpenAI
from diskcache import FanoutCache as Cache
from typing import Optional
import os

cache = None


def send_req(
    *,
    api_key,
    api_base,
    model,
    messages,
    **kwargs,
):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Failed to send request: {e}") from e


def to_llm(
    *,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: str,
    messages: list,
    cache_enabled: bool = True,
    cache_directory: str = "./.diskcache/oai_cache",
    **kwargs,
) -> str:
    global cache

    if cache_enabled and cache is None:
        cache = Cache(directory=cache_directory)

    api_key = api_key or os.getenv("OPENAI_API_KEY", "")
    api_base = api_base or os.getenv("OPENAI_API_BASE", "")

    if cache_enabled:
        cached_send_req = cache.memoize(typed=True)(send_req)
        chat_response = cached_send_req(
            model=model,
            messages=messages,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        chat_response = send_req(
            model=model,
            messages=messages,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )

    return chat_response


if __name__ == "__main__":
    result = to_llm(
        model="deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": "1+1=?",
            },
        ],
        max_tokens=1024,
        api_key="",
        api_base="",
    )
    print(f"result:{result}")
