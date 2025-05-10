import audio_recording as ar
import voice
import model
import utils.async_utils as au
import asyncio

async def main():
    
    messages: list = [
    {"role": "system", 
     "content": "Eres un asistente que da respuestas concisas y claras a diferentes preguntas."},
    {"role": "user",
     "content": "Hola, ¿cómo estás?"},]
    
    messages = await au.presentation(messages)

    while True:
        user_input = await au.async_audio_recording()
        print(f"Target: {user_input}")

        if not user_input:
            break
        
        await au.async_process_input(messages, user_input)

async def startup():
    await au.async_preload()
    await main()

if __name__ == "__main__":
    asyncio.run(startup())
    voice.shutdown_tts()
    ar.shutdown_audio()
    model.shutdown_model()