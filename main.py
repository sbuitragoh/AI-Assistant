import audio_recording as ar
import voice
import model
import torch as t
import asyncio
import logging

#logging.basicConfig(level=logging.INFO)

async def async_preload():
    global preloaded_device
    preloaded_device = t.device("cuda" if t.cuda.is_available() else "cpu")
    #logging.info(f"Using device: {preloaded_device}")
    model.preload_model()
    #logging.info("Model preloaded")
    voice.preload_tts(preloaded_device)
    #logging.info("TTS preloaded")
    ar.preload_audio()
    #logging.info("Audio preloaded")

async def async_model_inference(messages: list):
    return model.model(messages=messages)

async def async_audio_recording():
    return ar.target_creation()

async def async_voice_text_to_speech(text: str):
    await voice.voice_text_to_speech(text)

async def process_response(messages: list, response_gen):
    async for response in response_gen:
        messages.append({"role": "assistant", "content": response})
        await async_voice_text_to_speech(response)

async def presentation(messages: list) -> list:
    response_gen = await async_model_inference(messages)
    await process_response(messages, response_gen)
    return messages

async def async_process_input(messages: list, user_input: str):
    messages.append({"role": "user", "content": user_input})
    response_gen = await async_model_inference(messages)
    await process_response(messages, response_gen)

async def main():
    
    messages: list = [
    {"role": "system", 
     "content": "Eres un asistente que da respuestas concisas y claras a diferentes preguntas."},
    {"role": "user",
     "content": "Hola, ¿cómo estás?"},]
    
    messages = await presentation(messages)

    while True:
        user_input = await async_audio_recording()
        print(f"Target: {user_input}")

        if not user_input:
            break
        
        await asyncio.gather(async_process_input(messages, user_input))

if __name__ == "__main__":
    asyncio.run(async_preload())
    asyncio.run(main())
    voice.shutdown_tts()
    ar.shutdown_audio()
    model.shutdown_model()