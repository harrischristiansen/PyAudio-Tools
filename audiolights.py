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

LOW_TS = 30
HIGH_BRI = 230
LOW_BRI = 70

step1H	= FadeToColorAnimation(bothlights, [BLUE], brightness=HIGH_BRI, tsTime=1, sTime=0)
step2H	= FadeToColorAnimation(bothlights, [PURPLE], brightness=HIGH_BRI, tsTime=1, sTime=0)
step3H	= FadeToColorAnimation(bothlights, [ORANGE], brightness=HIGH_BRI, tsTime=1, sTime=0)
step4H	= FadeToColorAnimation(bothlights, [PINK], brightness=HIGH_BRI, tsTime=1, sTime=0)
step1L	= FadeToColorAnimation(bothlights, [YELLOW], brightness=LOW_BRI, tsTime=LOW_TS, sTime=0)
step2L	= FadeToColorAnimation(bothlights, [RED], brightness=LOW_BRI, tsTime=LOW_TS, sTime=0)
step3L	= FadeToColorAnimation(bothlights, [GREEN], brightness=LOW_BRI, tsTime=LOW_TS, sTime=0)
step4L	= FadeToColorAnimation(bothlights, [BROWN], brightness=LOW_BRI, tsTime=LOW_TS, sTime=0)

animations = [
	(step1L, step1H),
	(step2L, step2H),
	(step3L, step3H),
	(step4L, step4H)
]

# -------------------- Audio --------------------
import audiotk
import threading

LOW_FREQ = 1800
HIGH_FREQ = 3500

RUN_SECONDS = 250

class AudioLights(object):
	def __init__(self):
		self._frames = []
		self._animationStep = 0

	def animateAudio(self):
		# audiotk.get_audio_with_callback(RUN_SECONDS, self.checkData)
		for data in audiotk.get_audio(RUN_SECONDS):
			self.checkData(data)
		return self._frames

	def checkData(self, data, frame_count=None, time_info=None, status=None):
		self._frames.append(data)

		sample_freq = audiotk.freq_from_data(data)
		#logging.debug("The freq is %f Hz." % (sample_freq))

		if sample_freq > LOW_FREQ:
			self._spawn(self.advanceAnimation, sample_freq)

	def advanceAnimation(self, freq):
		anim_num = self._animationStep % len(animations)
		if freq > HIGH_FREQ:
			logging.info("Animation Advanced - High: %f" % freq)
			animations[anim_num][1].run()
		else:
			logging.info("Animation Advanced - Low: %f" % freq)
			animations[anim_num][0].run()
		self._animationStep += 1

	def _spawn(self, f, *args):
		t = threading.Thread(target=f, args=args)
		t.daemon = True
		t.start()

########################### Main ###########################
if __name__ == '__main__':
	audioLights = AudioLights()
	frames = audioLights.animateAudio()
	#audiotk.save_to_file("recording.wav", frames)
