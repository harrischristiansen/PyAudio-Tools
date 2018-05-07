# @ Harris Christiansen (code@harrischristiansen.com)
# Uses https://github.com/harrischristiansen/lightcontrol_py to animate lights to audio
# Available on GitHub: https://github.com/harrischristiansen/PyAudio-Tools

import logging
logging.basicConfig(level=logging.DEBUG)

# -------------------- Lights --------------------

from HueControls import HueControls
from LightControl import *

HUE_BRIDGE_IP = '192.168.1.125'
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
BROWN	= huecontrols.hexToXY("#FFFFFF")

globalLight	= [Light(huecontrols, 0, "All Lights", 0, 0)]
light1		= Light(huecontrols, 3, "Window", 0.5, 0.9)
light2		= Light(huecontrols, 5, "Couch", 0.5, 0.8)
bothlights = [light1, light2]

fadeToWhiteH	= FadeToColorAnimation(bothlights, [WHITE], brightness=255, tsTime=1, sTime=0)
fadeToWhiteL	= FadeToColorAnimation(bothlights, [WHITE], brightness=50, tsTime=40, sTime=0)
fadeToRedH		= FadeToColorAnimation(bothlights, [RED], brightness=255, tsTime=1, sTime=0)
fadeToRedL		= FadeToColorAnimation(bothlights, [RED], brightness=50, tsTime=40, sTime=0)
fadeToGreenH	= FadeToColorAnimation(bothlights, [GREEN], brightness=255, tsTime=1, sTime=0)
fadeToGreenL	= FadeToColorAnimation(bothlights, [GREEN], brightness=50, tsTime=40, sTime=0)
fadeToBlueH		= FadeToColorAnimation(bothlights, [BLUE], brightness=255, tsTime=1, sTime=0)
fadeToBlueL		= FadeToColorAnimation(bothlights, [BLUE], brightness=50, tsTime=40, sTime=0)

animations = [
	(fadeToWhiteL, fadeToWhiteH),
	(fadeToRedL, fadeToRedH),
	(fadeToGreenL, fadeToGreenH),
	(fadeToBlueL,fadeToBlueH)
]

# -------------------- Audio --------------------
import audiotk

LOW_FREQ = 3500
HIGH_FREQ = 7000

RUN_SECONDS = 250

class AudioLights(object):
	def __init__(self):
		self._frames = []
		self._animationStep = 0

	def animateAudio(self):
		for data in audiotk.get_audio(RUN_SECONDS):
			self.checkData(data)
		return self._frames

	def checkData(self, data):
		self._frames.append(data)

		sample_freq = audiotk.freq_from_data(data)
		#logging.debug("The freq is %f Hz." % (sample_freq))

		if sample_freq > LOW_FREQ:
			self.advanceAnimation(sample_freq)

	def advanceAnimation(self, freq):
		logging.debug("Animation Advanced %f" % freq)
		anim_num = self._animationStep % len(animations)
		if freq > HIGH_FREQ:
			animations[anim_num][1].run()
		else:
			animations[anim_num][0].run()
		self._animationStep += 1

########################### Main ###########################
if __name__ == '__main__':
	audioLights = AudioLights()
	frames = audioLights.animateAudio()
	#audiotk.save_to_file("recording.wav", frames)
