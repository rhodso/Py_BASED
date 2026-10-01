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

	def __eq__(self, other):
		if not isinstance(other, Soundboard_Sound):
			return NotImplemented

		return (
			self.name == other.name and
			self.is_file == other.is_file and
			self.vol == other.vol and
			self.tts == other.tts and
			self.fp == other.fp
		)

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
	def add_sb_btn(soundinfo : dict):
		L.log(f"Adding soundboard button", module="Soundboard_Manager")
		snd = Soundboard_Sound.from_dict(soundinfo)

		Soundboard_Manager.sb_btns.append(snd)
		Soundboard_Manager.save_sb_btns()

	@staticmethod
	def rm_sb_btn(soundinfo : dict):
		L.log(f"Removing soundboard button", module="Soundboard_Manager")
		snd = Soundboard_Sound.from_dict(soundinfo)

		tmp = Soundboard_Manager.sb_btns.copy()
		if snd in tmp:
			tmp.remove(snd)

		Soundboard_Manager.sb_btns = tmp
		Soundboard_Manager.save_sb_btns()
		

	@staticmethod
	def load_sb_btns():
		L.log(f"Loading soundboard buttons from {Soundboard_Manager.sb_btns_path}", module="Soundboard_Manager")

		Soundboard_Manager.sb_btns.clear()

		data = []
		with open(Soundboard_Manager.sb_btns_path, "r") as f:
			data = json.load(f)

		L.log(f"Found {len(data)} sounds. Loading...", module="Soundboard_Manager")

		for s in data:
			snd = Soundboard_Sound.from_dict(s)
			Soundboard_Manager.sb_btns.append(snd)
	
		L.log(f"Done loading sounds", module="Soundboard_Manager")		
	
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
	
