# from flask import Flask, render_template, request, jsonify
# import asyncio
# import pyaudio
# from pyaudio import Stream
# from amazon_transcribe.client import TranscribeStreamingClient
# from amazon_transcribe.handlers import TranscriptResultStreamHandler
# from amazon_transcribe.model import TranscriptEvent

# app = Flask(__name__)

# SAMPLE_RATE = 16000
# FRAMES_PER_BUFFER = 4096
# BYTES_PER_SAMPLE = 2
# CHANNEL_NUMS = 1
# REGION = "us-east-1"

# class MyEventHandler(TranscriptResultStreamHandler):
#     async def handle_transcript_event(self, transcript_event: TranscriptEvent):
#         results = transcript_event.transcript.results
#         for result in results:
#             for alt in result.alternatives:
#                 print(alt.transcript,"alt.transcript")

# async def basic_transcribe(audio_stream: Stream, sample_rate: int, chunk_size: int):
#     client = TranscribeStreamingClient(region=REGION)
#     stream = await client.start_stream_transcription(
#         language_code="en-US",
#         media_sample_rate_hz=sample_rate,
#         media_encoding="pcm",
#     )

#     async def write_chunks():
#         try:
#             while True:
#                 chunk = await asyncio.to_thread(audio_stream.read, chunk_size)
#                 if not chunk:
#                     break
#                 await stream.input_stream.send_audio_event(audio_chunk=chunk)
#                 await asyncio.sleep(chunk_size / sample_rate)
#             await stream.input_stream.end_stream()
#         except Exception as e:
#             print(f"An error occurred: {e}")

#     handler = MyEventHandler(stream.output_stream)
#     await asyncio.gather(write_chunks(), handler.handle_events())

# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/get_transcription_results')
# def get_transcription_results():
#     global transcription_result
#     return jsonify({'transcription': transcription_result})


# @app.route('/start_transcription', methods=['POST'])
# def start_transcription():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
    
#     p = pyaudio.PyAudio()
#     audio_stream = p.open(
#         frames_per_buffer=FRAMES_PER_BUFFER,
#         rate=SAMPLE_RATE,
#         format=pyaudio.paInt16,
#         channels=CHANNEL_NUMS,
#         input=True,
#     )

#     try:
#         loop.run_until_complete(basic_transcribe(audio_stream, SAMPLE_RATE, FRAMES_PER_BUFFER * BYTES_PER_SAMPLE * CHANNEL_NUMS))
#     finally:
#         loop.close()
    
#     return jsonify({'status': 'Transcription started'})

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, jsonify
import asyncio
import pyaudio
from pyaudio import Stream
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

app = Flask(__name__)

SAMPLE_RATE = 16000
FRAMES_PER_BUFFER = 4096
BYTES_PER_SAMPLE = 2
CHANNEL_NUMS = 1
REGION = "us-east-1"

transcription_result = ""  # Global variable to store transcription results

class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        global transcription_result
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                transcription_result = alt.transcript
                print(transcription_result)

async def basic_transcribe(audio_stream: Stream, sample_rate: int, chunk_size: int):
    client = TranscribeStreamingClient(region=REGION)
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=sample_rate,
        media_encoding="pcm",
    )

    async def write_chunks():
        try:
            while True:
                chunk = await asyncio.to_thread(audio_stream.read, chunk_size)
                if not chunk:
                    break
                await stream.input_stream.send_audio_event(audio_chunk=chunk)
                await asyncio.sleep(chunk_size / sample_rate)
            await stream.input_stream.end_stream()
        except Exception as e:
            print(f"An error occurred: {e}")

    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(), handler.handle_events())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_transcription_results')
def get_transcription_results():
    global transcription_result
    return jsonify({'transcription': transcription_result})

@app.route('/start_transcription', methods=['POST'])
def start_transcription():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    p = pyaudio.PyAudio()
    audio_stream = p.open(
        frames_per_buffer=FRAMES_PER_BUFFER,
        rate=SAMPLE_RATE,
        format=pyaudio.paInt16,
        channels=CHANNEL_NUMS,
        input=True,
    )

    try:
        loop.run_until_complete(basic_transcribe(audio_stream, SAMPLE_RATE, FRAMES_PER_BUFFER * BYTES_PER_SAMPLE * CHANNEL_NUMS))
    finally:
        loop.close()
    
    return jsonify({'status': 'Transcription started'})

if __name__ == '__main__':
    app.run(debug=True)
