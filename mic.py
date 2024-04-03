import asyncio
import pyaudio

from aws import basic_transcribe

SAMPLE_RATE = 16000
FRAMES_PER_BUFFER = 4096


p = pyaudio.PyAudio()
audio_stream = p.open(
    frames_per_buffer=FRAMES_PER_BUFFER,
    # input_device_index=1,
    rate=SAMPLE_RATE,
    format=pyaudio.paInt16,
    channels=1,
    input=True,
)

asyncio.run(
    basic_transcribe(
        audio_stream=audio_stream,
        sample_rate=SAMPLE_RATE,
        chunk_size=FRAMES_PER_BUFFER,
    )
)
