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
		L.log(f"Setting config path to {path}", module="ConfigManager")
		Config_Manager.config_path = path

	@staticmethod
	def load_config():
		L.log(f"Loading config from {Config_Manager.config_path}", module="ConfigManager")

		# Test if config file exists
		if not os.path.exists(Config_Manager.config_path):
			L.log("Config file does not exist, creating default config", level="warning", module="ConfigManager")
			Config_Manager.validate_config({})
			return

		tmp = {}
		with open(Config_Manager.config_path, "r") as f:
			try:
				tmp = json.load(f)
			except json.JSONDecodeError:
				L.log("Config file is not valid JSON, using empty config", level="warning", module="ConfigManager")
				tmp = {}
			
		# Null check
		Config_Manager.config = Config_Manager.validate_config(tmp)

		# Now actually set the values
		Audio_Device_Manager.set_output_device_id(Config_Manager.config['Output Device'])

	@staticmethod
	def validate_config(cfg):
		L.log("Validating config", module="ConfigManager")

		required_keys = {
			"Input Device": Audio_Device_Manager.get_default_input_device_idx(),
			"Output Device": Audio_Device_Manager.get_default_output_device_idx(),
			"Soundboard Columns": 5,
			"Max Queue Item Length": 27,
			"tts_volume": 1,
			"tts_len_scale": 1,
			"tts_noise_scale": 0.667,
			"tts_noise_wscale": 0.8,
			"tts_normalise": False
		}

		# Check if all required keys are present in config
		# Replace with default values if not present

		is_config_invalid = False

		for key, default_value in required_keys.items():
			if key not in cfg:
				is_config_invalid = True
				L.log(f"Config key '{key}' missing, setting to default value '{default_value}'", level="warning", module="ConfigManager")
				cfg[key] = default_value

		if is_config_invalid:
			L.log("Config is invalid, saving updated config with default values", level="warning", module="ConfigManager")
			Config_Manager.save_config(cfg)

		# Return cfg
		return cfg

	@staticmethod
	def save_config(cfg=None):
		if cfg is None:
			Config_Manager.config = cfg
			
		L.log(f"Saving config to {Config_Manager.config_path}", module="ConfigManager")
		with open(Config_Manager.config_path, "w") as f:
			json.dump(Config_Manager.config, f, indent=4)

	@staticmethod
	def update_config(field, value):
		L.log(f"Updating config field='{field}' and value='{value}", module="ConfigManager")
		if Config_Manager.config is None:
			Config_Manager.config = {}
			Config_Manager.load_config()

		# Check if key exists
		k = Config_Manager.config.keys()
		if field not in k:
			L.log(f"Field {field} not found in config dictionary", level="warning", module="ConfigManager")
			raise KeyError(f"Key '{field}' not found in config dictionary")
			return
		Config_Manager.config[field] = value
		L.log(f"Succesfully updated config, saving...", module="ConfigManager")
		Config_Manager.save_config(Config_Manager.config)
		L.log(f"Saved config", module="ConfigManager")
