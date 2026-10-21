import json
import time

from openai import OpenAI

from . import config
from .prompts import SYSTEM_PROMPT


client = OpenAI(
    base_url=config.VLLM_BASE_URL,
    api_key=config.VLLM_API_KEY,
)


def call_llm(text: str, model: str | None = None) -> dict:
    model_name = model or config.MODEL

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        temperature=config.TEMPERATURE,
        max_tokens=config.MAX_TOKENS,
    )

    latency_ms = int(
        (time.perf_counter() - start_time) * 1000
    )

    content = response.choices[0].message.content
    
    raw = json.loads(content)

    return {
        "raw": raw,
        "model": model_name,
        "latency_ms": latency_ms,
        "input_tokens": (
            response.usage.prompt_tokens
            if response.usage else 0
        ),
        "output_tokens": (
            response.usage.completion_tokens
            if response.usage else 0
        ),
        "cost": 0.0,
    }