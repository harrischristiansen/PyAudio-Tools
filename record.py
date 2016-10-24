import math
import numpy
import pyaudio
import wave

RECORD_SECONDS = 3
FORMAT = pyaudio.paInt16
NUM_CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024

def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return numpy.sin(numpy.arange(length) * factor)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=NUM_CHANNELS, rate=RATE, input=1, frames_per_buffer=CHUNK_SIZE)

frames = []
for i in range(0, (RATE/CHUNK_SIZE) * RECORD_SECONDS):
	data = stream.read(CHUNK_SIZE)
	frames.append(data)

stream.close()
p.terminate()

wf = wave.open("test.wav", 'wb')
wf.setnchannels(NUM_CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()