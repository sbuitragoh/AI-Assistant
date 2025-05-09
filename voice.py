import torch as t
from RealtimeTTS import CoquiEngine, TextToAudioStream # type: ignore
from utils.constants import LANGUAGE, OUTPUT_AUDIO, TARGET_AUDIO

tts_engine = None
tts_stream = None

def preload_tts(device):
    global tts_engine, tts_stream
    if tts_engine is None:
        tts_engine = CoquiEngine(device=device, language=LANGUAGE, voice=TARGET_AUDIO)
        tts_stream = TextToAudioStream(engine=tts_engine, language=LANGUAGE)


async def voice_text_to_speech(text: str) -> None:

    if tts_engine is None or tts_stream is None:
        raise RuntimeError("TTS engine and stream must be preloaded before use.")

    tts_stream.feed(text).play(log_synthesized_text = True,
                            language=LANGUAGE,
                            output_wavfile=OUTPUT_AUDIO)
    tts_stream.stop()

def shutdown_tts():
    global tts_engine, tts_stream
    if tts_engine is not None:
        tts_engine.shutdown()
        tts_engine = None
        tts_stream = None