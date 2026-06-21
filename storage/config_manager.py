import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from audio.devices import Audio_Device_Manager

class Config_Manager:
	config_path = "config/config.json"
	config = {}
	
	@staticmethod
	def set_config_path(path):
		L.log(f"Setting config path to {path}", module="Config_Manager")
		Config_Manager.config_path = path

	@staticmethod
	def load_config():
		L.log(f"Loading config from {Config_Manager.config_path}", module="Config_Manager")

		# Test if config file exists
		if not os.path.exists(Config_Manager.config_path):
			L.log("Config file does not exist, creating default config", level="warning", module="Config_Manager")
			Config_Manager.validate_config({})
			return

		tmp = {}
		with open(Config_Manager.config_path, "r") as f:
			try:
				tmp = json.load(f)
			except json.JSONDecodeError:
				L.log("Config file is not valid JSON, using empty config", level="warning", module="Config_Manager")
				tmp = {}
			
		# Null check
		Config_Manager.config = Config_Manager.validate_config(tmp)

	@staticmethod
	def validate_config(cfg):
		L.log("Validating config", module="Config_Manager")

		required_keys = {
			"Input Device": Audio_Device_Manager.get_default_input_device_idx(),
			"Output Device": Audio_Device_Manager.get_default_output_device_idx(),
			"Soundboard Columns": 5,
			"Max Queue Item Length": 27,
			"tts_volume": 1,
			"tts_len_scale": 1,
			"tts_noise_scale": 1,
			"tts_noise_wscale": 1,
			"tts_normalise": False
		}

		# Check if all required keys are present in config
		# Replace with default values if not present

		is_config_invalid = False

		for key, default_value in required_keys.items():
			if key not in cfg:
				is_config_invalid = True
				L.log(f"Config key '{key}' missing, setting to default value '{default_value}'", level="warning", module="Config_Manager")
				cfg[key] = default_value

		if is_config_invalid:
			L.log("Config is invalid, saving updated config with default values", level="warning", module="Config_Manager")
			Config_Manager.save_config(cfg)

		# Return cfg
		return cfg

	@staticmethod
	def save_config(cfg=None):
		if cfg is not None:
			Config_Manager.config = cfg
			
		L.log(f"Saving config to {Config_Manager.config_path}", module="Config_Manager")
		with open(Config_Manager.config_path, "w") as f:
			json.dump(Config_Manager.config, f, indent=4)

