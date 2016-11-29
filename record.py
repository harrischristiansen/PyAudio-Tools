import math
import numpy as np
import pyaudio
import wave

RECORD_SECONDS = 50
FORMAT = pyaudio.paInt16
NUM_CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024

# Create Input Stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=NUM_CHANNELS, rate=RATE, input=1, frames_per_buffer=CHUNK_SIZE)

# Read input Stream
frames = []
window = np.blackman(CHUNK_SIZE)
swidth = p.get_sample_size(FORMAT)
for i in range(0, (RATE/CHUNK_SIZE) * RECORD_SECONDS):
	data = stream.read(CHUNK_SIZE)
	frames.append(data)

	indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window

	fftData = abs(np.fft.rfft(indata))**2

	which = fftData[1:].argmax() + 1
	
	sample_freq = which*RATE/CHUNK_SIZE

	if which != len(fftData)-1:
		y0,y1,y2 = np.log(fftData[which-1:which+2:])
		x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
		# find the frequency and output it
		sample_freq = (which+x1)*RATE/CHUNK_SIZE
	
	#print "The freq is %f Hz." % (sample_freq)
	if (sample_freq > 1100 and sample_freq < 1300):
		print "Permitted"

# Close Input Stream
stream.close()
p.terminate()

# Save to File
wf = wave.open("test.wav", 'wb')
wf.setnchannels(NUM_CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

########################### Helper Methods ###########################

def sine(frequency, length, rate):
	length = int(length * rate)
	factor = float(frequency) * (math.pi * 2) / rate
	return np.sin(numpy.arange(length) * factor)