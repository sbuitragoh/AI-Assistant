import ollama
import re
from utils.constants import MODEL_NAME

async def model(messages: list[dict]):
    response = ollama.chat(model=MODEL_NAME, messages=messages)
    answer: str = response.message.content
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)
    chunks = re.split(r'(?<=[.!?])/s+', answer)
    for chunk in chunks:
        yield chunk
