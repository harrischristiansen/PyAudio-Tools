import math
import numpy
import pyaudio

NUM_CHANNELS = 1
RATE = 44100

def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=440, length=1, rate=RATE):
	chunks = []
	chunks.append(sine(frequency, length, rate))

	chunk = numpy.concatenate(chunks) * 0.25
	stream.write(chunk.astype(numpy.float32).tostring())


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=NUM_CHANNELS, rate=RATE, output=1)

frequencies = [400,600,300,600,400,600,500,600,400,600,700,600]

for frequency in frequencies:
	play_tone(stream, frequency=frequency, length=0.05)

stream.close()
p.terminate()