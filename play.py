import math
import numpy
import pyaudio

NUM_CHANNELS = 1
RATE = 44100
DEFAULT_LENGTH = 0.05

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

frequencies = [400,[600,0.1],300,[600,0.02],[400,0.02],[600,0.02],500,600,400,[600,0.08],[700,0.08],[600,0.08]]

for frequency in frequencies:
	if isinstance(frequency, list): # Permit custom length
		play_tone(stream, frequency=frequency[0], length=frequency[1])
	else: # Use Default Length
		play_tone(stream, frequency=frequency, length=DEFAULT_LENGTH)

stream.close()
p.terminate()