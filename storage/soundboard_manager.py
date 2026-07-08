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

		return s

class Soundboard_Manager:
	sb_btns_path = "config/sb.json"
	sb_btns = []
	
	@staticmethod
	def load_sb_btns():
		L.log(f"Loading soundboard buttons from {Soundboard_Manager.sb_btns_path}", module="Soundboard_Manager")
		data = []
		with open(Soundboard_Manager.sb_btns_path, "r") as f:
			data = json.load(f)

		L.log(f"Found {len(data)} sounds. Loading...")

		for s in data:
			snd = Soundboard_Sound.from_dict(s)
			Soundboard_Manager.sb_btns.append(snd)
	
		L.log(f"Done loading sounds")		
	
	@staticmethod
	def save_sb_btns():
		L.log(f"Saving soundboard buttons to {Soundboard_Manager.sb_btns_path}", module="Soundboard_Manager")

		l = []
		for s in Soundboard_Manager.sb_btns:
			if isinstance(s, Soundboard_Sound):
				l.append(s.to_dict())

		with open(Soundboard_Manager.sb_btns_path, "w") as f:
			f.write(json.dumps(l))			

if __name__ == "__main__":
	manager = Soundboard_Manager()
	manager.load_sb_btns()
	
