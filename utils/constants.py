import re
from typing import Pattern

MODEL_NAME: str = "qwen3:14b"
TARGET_AUDIO: str = 'target/audio_target.wav'
OUTPUT_AUDIO: str = 'output/output.wav'
LANGUAGE: str = 'es'
RECON_LAN: str = 'es-ES'
TIME: int = 10
THINK_RE: Pattern = re.compile(r"<think>.*?</think>", flags=re.DOTALL)