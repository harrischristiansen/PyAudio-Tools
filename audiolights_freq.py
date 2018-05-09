# @ Harris Christiansen (code@harrischristiansen.com)
# Uses https://github.com/harrischristiansen/lightcontrol_py to animate lights to audio
# Available on GitHub: https://github.com/harrischristiansen/PyAudio-Tools

import logging
logging.basicConfig(level=logging.INFO)

# -------------------- Lights --------------------

from HueControls import HueControls
from LightControl import *

# HUE_BRIDGE_IP = '10.3.0.177' # Fuse
# HUE_BRIDGE_API_KEY = 'd5orxbetHKF46FCV1wBmnFTVNSkGQWMSjwNOHu2i'
HUE_BRIDGE_IP = '192.168.1.125' # Namans
HUE_BRIDGE_API_KEY = 'QeU9qwKYDc5Z1OqzhPMbrutdRwSKj9wDFgLUAii4'
huecontrols = HueControls(HUE_BRIDGE_IP, HUE_BRIDGE_API_KEY)
huecontrols.startLightQueue()

WHITE	= huecontrols.hexToXY("#FFFFFF")
RED		= huecontrols.hexToXY("#FF0000")
GREEN	= huecontrols.hexToXY("#00FF00")
BLUE	= huecontrols.hexToXY("#0000FF")
ORANGE	= huecontrols.hexToXY("#904000")
PINK	= huecontrols.hexToXY("#800080")
YELLOW	= huecontrols.hexToXY("#ffb400")
PURPLE	= huecontrols.hexToXY("#bb00ff")
CYAN	= huecontrols.hexToXY("#FFFFFF")
BROWN	= huecontrols.hexToXY("#aa6000")

globalLight	= [Light(huecontrols, 0, "All Lights", 0, 0)]
light1		= Light(huecontrols, 3, "Bulb", 0.5, 0.9) # 17=bathroom, 28=counter
light2		= Light(huecontrols, 5, "Strip", 0.5, 0.8)
bothlights = [light1, light2]

step1	= FadeToColorAnimation(bothlights, [BLUE], brightness=50, tsTime=30, sTime=0)
step2	= FadeToColorAnimation(bothlights, [PURPLE], brightness=70, tsTime=25, sTime=0)
step3	= FadeToColorAnimation(bothlights, [PINK], brightness=100, tsTime=20, sTime=0)
step4	= FadeToColorAnimation(bothlights, [RED], brightness=130, tsTime=15, sTime=0)
step5	= FadeToColorAnimation(bothlights, [BROWN], brightness=160, tsTime=10, sTime=0)
step6	= FadeToColorAnimation(bothlights, [ORANGE], brightness=190, tsTime=5, sTime=0)
step7	= FadeToColorAnimation(bothlights, [YELLOW], brightness=220, tsTime=2, sTime=0)
step8	= FadeToColorAnimation(bothlights, [WHITE], brightness=255, tsTime=1, sTime=0)

animations = [step1, step2, step3, step4, step5, step6, step7, step8]

# -------------------- Audio --------------------
import audiotk

RUN_SECONDS = 1000
MAX_FREQ = 8000
LEN_ANIMATIONS = len(animations)
FREQ_PER_STEP = MAX_FREQ/LEN_ANIMATIONS

class AudioLights(object):
	def __init__(self):
		self._frames = []
		self._lastStep = 0

	def animateAudio(self):
		audiotk.get_audio_with_callback(RUN_SECONDS, self.checkData)
		return self._frames

	def checkData(self, data, frame_count=None, time_info=None, status=None):
		self._frames.append(data)

		sample_freq = audiotk.freq_from_data(data)
		#logging.debug("The freq is %f Hz." % (sample_freq))

		self.advanceAnimation(sample_freq)

		return (data, audiotk.pyaudio.paContinue)

	def advanceAnimation(self, freq):
		step = int(freq/FREQ_PER_STEP)
		if step >= LEN_ANIMATIONS:
			step = LEN_ANIMATIONS - 1

		if step != self._lastStep:
			logging.info("Rendering Step: %d with freq %d" % (step, freq))
			animations[step].run()
			self._lastStep = step

########################### Main ###########################
if __name__ == '__main__':
	audioLights = AudioLights()
	frames = audioLights.animateAudio()
	#audiotk.save_to_file("recording.wav", frames)
	huecontrols.stopLightQueue()
