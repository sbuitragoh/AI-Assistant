import ollama
import re
import asyncio
from utils.constants import MODEL_NAME, THINK_RE

preloaded_model = None

def preload_model():
    """Preload the model. This function is a placeholder and does not perform any action."""
    global preloaded_model
    if preloaded_model is None:
        preloaded_model = ollama

async def model(messages: list[dict]):

    if preloaded_model is None:
        raise RuntimeError("Model must be preloaded before use.")

    response = await asyncio.to_thread(
        preloaded_model.chat, model=MODEL_NAME, messages=messages
    )
    # Access the response as a dictionary
    answer: str = response["message"]["content"]
    answer = THINK_RE.sub("", answer)
    chunks = re.split(r'(?<=[.!?])\s+', answer)
    for chunk in chunks:
        yield chunk

def shutdown_model():
    global preloaded_model
    preloaded_model = None