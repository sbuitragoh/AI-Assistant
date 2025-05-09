import audio_recording as ar
import voice
import model
import torch as t
import asyncio

async def async_model_inference(messages):
    return model.model(messages=messages)

async def async_audio_recording():
    return ar.target_creation()

async def async_voice_text_to_speech(device, text):
    await asyncio.to_thread(voice.voice_text_to_speech, device, text)

async def presentation(device, messages: list) -> list:
    response_gen = await async_model_inference(messages)
    async for response in response_gen:
        messages.append({"role": "assistant", "content": response})
        await async_voice_text_to_speech(device, response)
    return messages

async def main():
    device = t.device('cuda' if t.cuda.is_available() else 'cpu')
    
    messages: list = [
    {"role": "system", 
     "content": "Eres un asistente que da respuestas concisas y claras a diferentes preguntas."},
    {"role": "user",
     "content": "Hola, ¿cómo estás?"},]
    
    messages = await presentation(device, messages)

    while True:
        target = await async_audio_recording()
        print(f"Target: {target}")

        user_input = target
        if not user_input:
            break
        messages.append({"role": "user", "content": user_input})
        response_gen = await async_model_inference(messages)
        async for response in response_gen:
            messages.append({"role": "assistant", "content": response})
            await async_voice_text_to_speech(device, response)

if __name__ == "__main__":
    asyncio.run(main())