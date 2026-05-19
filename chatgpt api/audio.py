from pathlib import Path
import os
from openai import OpenAI

client = OpenAI()

# サンプル音声の文字起こし
audio_path = Path("./sample_audio.mp3")

with audio_path.open("rb") as f:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=f, temperature=0.0
    )
print(transcription.text)

prompt = "下垣内"

with audio_path.open("rb") as f:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        prompt=prompt,
        response_format="text",
        temperature=0.0
    )
print(transcription)

#　音声合成
audio_output_path = Path("output.mp3")
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="こんにちは。私はAIアシスタントです!",
) as response:
    response.stream_to_file(audio_output_path)

print(audio_output_path.resolve())

os.startfile(audio_output_path)