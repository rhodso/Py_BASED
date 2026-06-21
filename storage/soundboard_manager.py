import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L

class Soundboard_Sound:
	def __init__(self):
		self.name = ""
		self.is_file = None
		self.fp = None
		self.tts = None
		self.icon_fp = None
		self.vol = 1.0

	def to_dict(self):
		return {
			"name": self.name,
			"is_file": self.is_file,
			"fp": self.fp,
			"tts_text": self.tts,
			"icon_fp": self.icon_fp,
			"vol": self.vol
		}
	
	@staticmethod
	def from_dict(d):
		s = Soundboard_Sound()

		s.name = d.get("name", "")
		s.is_file = d.get("is_file", None)
		s.fp = d.get("fp", None)
		s.tts = d.get("tts_text", None)
		s.icon_fp = d.get("icon_fp", None)
		s.vol = d.get("vol", 1.0)

class Soundboard_Manager:
	sb_btns_path = "config/sb.json"
	sb_btns = []
	
	@staticmethod
	def load_sb_btns():
		L.log(f"Loading soundboard buttons from {Soundboard_Manager.sb_btns_path}", module="Soundboard_Manager")
		with open(Soundboard_Manager.sb_btns_path, "r") as f:
			Soundboard_Manager.sb_btns = json.load(f)
	
	@staticmethod
	def save_sb_btns():
		L.log(f"Saving soundboard buttons to {Soundboard_Manager.sb_btns_path}", module="Soundboard_Manager")
		with open(Soundboard_Manager.sb_btns_path, "w") as f:
			json.dump(Soundboard_Manager.sb_btns, f, indent=4)

