# @ Harris Christiansen (code@harrischristiansen.com)
# Available on GitHub: https://github.com/harrischristiansen/PyAudio-Tools

import math
import numpy as np
import pyaudio
import time
import wave

FORMAT = pyaudio.paInt16
NUM_CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024
DEFAULT_LENGTH = 0.05

p = pyaudio.PyAudio()

########################### Audio IO ###########################

def get_audio(num_seconds):
	# Create Input Stream
	stream = p.open(format=FORMAT, channels=NUM_CHANNELS, rate=RATE, input=1, frames_per_buffer=CHUNK_SIZE)

	# Read input Stream
	for i in range(0, int(RATE/CHUNK_SIZE) * num_seconds):
		data = stream.read(CHUNK_SIZE)
		yield data

	# Close Input Stream
	stream.close()

def get_audio_with_callback(num_seconds, callback):
	# Create Input Stream
	stream = p.open(format=FORMAT, channels=NUM_CHANNELS, rate=RATE, input=1, frames_per_buffer=CHUNK_SIZE, stream_callback=callback)
	stream.start_stream()

	# Wait for num_seconds
	time.sleep(num_seconds)

	# Close Input Stream
	stream.stop_stream()
	stream.close()

def play_tone(stream, frequency=440, length=DEFAULT_LENGTH, rate=RATE):
	chunks = []
	chunks.append(sine(frequency, length, rate))

	chunk = np.concatenate(chunks) * 0.25
	stream.write(chunk.astype(np.float32).tostring())
	return chunk.astype(np.float32)

def play_pattern(pattern):
	stream = p.open(format=pyaudio.paFloat32, channels=NUM_CHANNELS, rate=RATE, output=1)

	frames = []
	for frequency in pattern:
		if isinstance(frequency, list): # Permit custom length
			frames.append(play_tone(stream, frequency=frequency[0], length=frequency[1]))
		else: # Use Default Length
			frames.append(play_tone(stream, frequency=frequency))

	stream.close()
	return frames

########################### Determine Frequency from input data ###########################

window = np.blackman(CHUNK_SIZE)
swidth = p.get_sample_size(FORMAT)
def freq_from_data(data):
	indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window
	fftData = abs(np.fft.rfft(indata))**2
	which = fftData[1:].argmax() + 1
	sample_freq = which*RATE/CHUNK_SIZE

	if which != len(fftData)-1:
		y0,y1,y2 = np.log(fftData[which-1:which+2:])
		x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
		sample_freq = (which+x1)*RATE/CHUNK_SIZE

	return sample_freq

########################### File IO ###########################

def save_to_file(fileName, frames):
	wf = wave.open(fileName, 'wb')
	wf.setnchannels(NUM_CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

########################### Math ###########################

def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return np.sin(np.arange(length) * factor)