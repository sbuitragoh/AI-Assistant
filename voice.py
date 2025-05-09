import torch as t
from RealtimeTTS import CoquiEngine, TextToAudioStream
from utils.constants import LANGUAGE, OUTPUT_AUDIO, TARGET_AUDIO

def voice_text_to_speech(device, text: str) -> None:

    engine = CoquiEngine(device=device, language=LANGUAGE, voice=TARGET_AUDIO)
    stream = TextToAudioStream(engine=engine, language=LANGUAGE)
    stream.feed(text).play(log_synthesized_text = True,
                            language=LANGUAGE,
                            output_wavfile=OUTPUT_AUDIO)
    stream.stop()
    engine.shutdown()

