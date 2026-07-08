import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L

from audio.devices import Audio_Device_Manager
from tts.tts import TTS_Engine

import sounddevice as sd

class Audio_Engine:

	@staticmethod
	def play_text(text):
		L.log(f"Playing text {text}", module="AudioEngine")
		idx = Audio_Device_Manager.current_output_device_id

		# Null check
		if idx < 0:
			idx = Audio_Device_Manager.get_default_output_device_idx()
		
		try:
			L.log("Attemting to generate text", module="AudioEngine")
			samples, sample_rate = TTS_Engine.gen(text)
		except Exception as e:
			print("Audio generation failed")
			print(f"{e}")

			L.log("Audo Generation failed", "error", module="AudioEngine")
			L.log(f"Details: {e}", "error", module="AudioEngine")
			return
		
		L.log("Generation succeeded, playing", module="AudioEngine")
		sd.default.samplerate = sample_rate
		sd.default.device = idx
		sd.play(samples, samplerate=sample_rate)
		L.log("Playback started", module="AudioEngine")
		sd.wait()

	@staticmethod
	def stop():
		L.log("Playback stopped early", module="AudioEngine")
		sd.stop()

if __name__ == "__main__":
	Audio_Engine.play_text("Here's some text")

