import sys
import os

import sounddevice as sd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L

class Audio_Device_Manager:
	devices = []

	@staticmethod
	def get_audio_devices():
		L.log("Getting audio devices", module="Audio_Device_Manager")
		devices = sd.query_devices()
		Audio_Device_Manager.devices = devices
		return devices
	
	@staticmethod
	def get_default_output_device_idx():
		L.log("Getting default output audio device", module="Audio_Device_Manager")
		if not Audio_Device_Manager.devices:
			Audio_Device_Manager.get_audio_devices()
		device = sd.default.device[1]  # Output device is index 1
		return device

	@staticmethod
	def get_default_input_device_idx():
		L.log("Getting default input audio device", module="Audio_Device_Manager")
		if not Audio_Device_Manager.devices:
			Audio_Device_Manager.get_audio_devices()
		device = sd.default.device[0]  # Input device is index 0
		return device

if __name__ == "__main__":
	L.setup()
	L.log("Testing Audio_Device_Manager", module="Audio_Device_Manager")

	print("\nDefault Output Device:")
	default_output_device_idx = Audio_Device_Manager.get_default_output_device_idx()
	default_output_device = Audio_Device_Manager.devices[default_output_device_idx]
	print(f"{default_output_device['name']}:")
	for k, v in default_output_device.items():
		print(f"{k}: {v}")

	print("\nDefault Input Device:")
	default_input_device_idx = Audio_Device_Manager.get_default_input_device_idx()
	default_input_device = Audio_Device_Manager.devices[default_input_device_idx]
	print(f"{default_input_device['name']}:")
	for k, v in default_input_device.items():
		print(f"{k}: {v}")

