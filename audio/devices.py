import sys
import os

import sounddevice as sd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L

class Audio_Device_Manager:
	devices = []
	current_output_device_id = -1

	@staticmethod
	def set_output_device_id(new_out_id):
		Audio_Device_Manager.current_output_device_id=new_out_id

	@staticmethod
	def get_audio_devices():
		L.log("Getting audio devices", module="AudioDeviceManager")
		devices = sd.query_devices()
		Audio_Device_Manager.devices = devices
		return devices
	
	@staticmethod
	def get_default_output_device_idx():
		L.log("Getting default output audio device", module="AudioDeviceManager")
		if not Audio_Device_Manager.devices:
			Audio_Device_Manager.get_audio_devices()
		device = sd.default.device[1]  # Output device is index 1
		return device

	@staticmethod
	def get_default_input_device_idx():
		L.log("Getting default input audio device", module="AudioDeviceManager")
		if not Audio_Device_Manager.devices:
			Audio_Device_Manager.get_audio_devices()
		device = sd.default.device[0]  # Input device is index 0
		return device

	@staticmethod
	def get_in_out(dev_id):
		o_dev = False
		i_dev = False

		try:
			# If the function does nothing, it's an input device
			# If it throws an exception, it's not
			sd.check_input_settings(dev_id)
			i_dev = True
		except: 
			pass

		try:
			sd.check_output_settings(dev_id)
			o_dev = True
		except:
			pass

		return [i_dev, o_dev]


if __name__ == "__main__":
	L.setup()
	L.log("Testing Audio_Device_Manager", module="AudioDeviceManager")

	devs = Audio_Device_Manager.get_audio_devices()
	o_dev = []
	i_dev = []

	for d in devs:
		l = Audio_Device_Manager.get_in_out(d['index'])
		if(l[0]):
			i_dev.append(d)
		if(l[1]):
			o_dev.append(d)
	
	print(o_dev)