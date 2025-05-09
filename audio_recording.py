import speech_recognition as sr
import pyaudio as pa
import wave
from utils.constants import TARGET_AUDIO, TIME, RECON_LAN

def audio_recording() -> None:
    chunk: int = 1024
    sample_format = pa.paInt16
    channels: int = 1
    fs: int = 22050
    seconds = TIME
    filename = TARGET_AUDIO

    p = pa.PyAudio()

    print('Recording...')
    stream = p.open(format=sample_format, channels=channels,
                    rate=fs, input=True,
                    frames_per_buffer=chunk)
    frames = []
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Recording finished')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def target_creation() -> str:

    audio_recording()
    audio = sr.AudioFile(TARGET_AUDIO)
    recon = sr.Recognizer()

    with audio as source:        
        recon.adjust_for_ambient_noise(source=source, duration=0.5)
        audio = recon.record(source)
        
        try:
            return recon.recognize_google(audio, language=RECON_LAN)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")