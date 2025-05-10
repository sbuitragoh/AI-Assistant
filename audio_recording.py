import speech_recognition as sr # type: ignore
import pyaudio as pa #type: ignore
import wave
from utils.constants import TARGET_AUDIO, TIME, RECON_LAN

audio_instance = None
recognizer = None

def preload_audio():
    global audio_instance, recognizer
    if audio_instance is None:
        audio_instance = pa.PyAudio()
    if recognizer is None:
        recognizer = sr.Recognizer()

def save_file(filename: str, channels: int, sample_format, fs: int,
              frames: list[bytes]):
    global audio_instance
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio_instance.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))

def audio_recording():
    if audio_instance is None:
        raise RuntimeError("Audio instance must be preloaded before use.")

    chunk: int = 2048
    sample_format = pa.paInt16
    channels: int = 1
    fs: int = 22050
    seconds: int = TIME
    filename: str = TARGET_AUDIO

    print('Recording...')
    stream = audio_instance.open(format=sample_format, channels=channels,
                    rate=fs, input=True,
                    frames_per_buffer=chunk)
    
    num_chunks = int(fs / chunk * seconds)
    frames = [stream.read(chunk) for _ in range(num_chunks)]

    stream.stop_stream()
    stream.close()
    print('Recording finished')

    save_file(filename, channels, sample_format, fs, frames)

def target_creation() -> str:

    if recognizer is None:
        raise RuntimeError("Recognizer must be preloaded before use.")

    audio_recording()
    audio_file = sr.AudioFile(TARGET_AUDIO)

    with audio_file as source:        
        recognizer.adjust_for_ambient_noise(source=source, duration=0.5)
        audio_data = recognizer.record(source)
        
        try:
            return recognizer.recognize_google(audio_data, language=RECON_LAN)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def shutdown_audio():
    global audio_instance
    if audio_instance is not None:
        audio_instance.terminate()
        audio_instance = None