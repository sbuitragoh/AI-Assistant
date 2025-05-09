import ollama
import re
from utils.constants import MODEL_NAME

preloaded_model = None

def preload_model():
    """Preload the model. This function is a placeholder and does not perform any action."""
    global preloaded_model
    if preloaded_model is None:
        preloaded_model = ollama

async def model(messages: list[dict]):

    if preloaded_model is None:
        raise RuntimeError("Model must be preloaded before use.")

    response = preloaded_model.chat(model=MODEL_NAME, messages=messages)
    answer: str = response.message.content
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)
    chunks = re.split(r'(?<=[.!?])\s+', answer)
    for chunk in chunks:
        yield chunk

def shutdown_model():
    global preloaded_model
    if preloaded_model is not None:
        preloaded_model = None