import os
import sys

import wave
import numpy as np
from piper import PiperVoice, SynthesisConfig

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from storage.config_manager import Config_Manager

class TTS_Engine:
	voice = None
	is_init = False

	@staticmethod
	def startup():
		TTS_Engine.is_init = True
		v = TTS_Engine.list_voices()
		TTS_Engine.load_voice(v[0]) # Load the 1st one by default

	@staticmethod
	def gen(text):
		if(not TTS_Engine.is_init):
			TTS_Engine.startup()

		L.log(f"Generating TTS for text: {text}", module="TTS_Engine")

		if not isinstance(TTS_Engine.voice, PiperVoice):
			L.log(f"Voice not loaded, could not generate text", "warn", module="TTS_Engine")
			raise Exception

		# Audio vars
		audio_bytes = bytearray()
		sample_rate = None

		# If the text doesn't end with '.', add one
		if(text[-1] != "."):
			text += "."

		# check the ConfigManager didn't screw up
		if Config_Manager.config == None or not isinstance(Config_Manager.config, dict) or Config_Manager.config == {}:
			Config_Manager.load_config()

			if not isinstance(Config_Manager.config, dict):
				raise ValueError(f"ConfigManager Config not a dict!")
				return

		syn_conf = SynthesisConfig()
		syn_conf.length_scale = Config_Manager.config['tts_len_scale']
		syn_conf.noise_scale = Config_Manager.config['tts_noise_scale']
		syn_conf.noise_w_scale = Config_Manager.config['tts_noise_wscale']

		for chunk in TTS_Engine.voice.synthesize(text, syn_conf):
			sample_rate = chunk.sample_rate
			audio_bytes.extend(chunk.audio_int16_bytes)
		samples = np.frombuffer(audio_bytes, dtype=np.int16)
		
		return samples, sample_rate

	@staticmethod
	def gen_file(text, fp):
		if(not TTS_Engine.is_init):
			TTS_Engine.startup()
		L.log(f"Generating TTS for text: {text} and saving to {fp}", module="TTS_Engine")
		
		voice = PiperVoice.load("voices/en_GB-cori-high.onnx")
		with wave.open(fp, "wb") as wav_file:
			voice.synthesize_wav(text, wav_file)

	@staticmethod
	def list_voices():
		if(not TTS_Engine.is_init):
			TTS_Engine.startup()
		# Get all files in dir
		p = "voices"
		dir_list = os.listdir(p)

		v = []
		for f in dir_list:    # remove file endings
			f = f.replace(".json", "")
			f = f.replace(".onnx", "")
			v.append(f)

		# Since they're all called the same thing, just remove duplicates and return the file names
		return list(set(v))
		

	@staticmethod
	def load_voice(v):
		if(not TTS_Engine.is_init):
			TTS_Engine.startup()
		L.log(f"Loading voice {v}", module="TTS_Engine")

		# Ensure v is a path that exists
		if os.path.isfile(f"voices/{v}.onnx"):
			L.log(f"{v}.onnx exists")
			if os.path.isfile(f"voices/{v}.onnx.json"):
				L.log(f"{v}.onnx.json exists")
				try:						
					TTS_Engine.voice = PiperVoice.load(f"voices/{v}.onnx")
				except Exception as e:
					L.log(f"Voice {v} could not be loaded")
					L.log(f"Error details: {e}")					
					return				
				L.log(f"voice {v} loaded")
			else:
				L.log(f"{v}.onnx.json does not exist, failed to load voice", "error", module="TTS_Engine")
		else:
			L.log(f"{v}.onnx does not exist, failed to load voice", "error", module="TTS_Engine")

if __name__ == "__main__":
	from audio.devices import Audio_Device_Manager
	import sounddevice as sd

	idx = Audio_Device_Manager.get_default_output_device_idx()
	dev = Audio_Device_Manager.devices[idx]
	
	try:
		samples, sample_rate = TTS_Engine.gen("This is a message to test the TTS engine")
	except Exception as e:
		print("Audio generation failed")
		print(f"{e}")
		exit(0)
		
	if not isinstance(TTS_Engine.voice, PiperVoice):
		exit(1)
	
	print(TTS_Engine.voice.config)

	sd.default.samplerate = sample_rate
	sd.default.device = idx
	sd.play(samples, samplerate=sample_rate)
	sd.wait()

