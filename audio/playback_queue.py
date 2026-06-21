import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from storage.soundboard_manager import Soundboard_Sound
from storage.config_manager import Config_Manager

class Queue_Item:
	def __init__(self, _name, _is_file, _vol, _tts = None, _fp = None):

		self.name = _name
		self.is_file = _is_file
		self.vol = _vol
		self.tts = _tts
		self.fp = _fp
		
	@staticmethod
	def from_SS(ss):
		
		if not isinstance(ss, Soundboard_Sound):
			return None
		
		itm = Queue_Item(
			_name = ss.name,
			_is_file = ss.is_file, 
			_vol = ss.vol,
			_tts = ss.tts, 
			_fp = ss.fp
		)
		return itm
	
	def to_str(self):
		max_length = Config_Manager.config.get(
			"Max Queue Item Length", 27) # Max queue item length
		s = ""

		# If is_file
		if self.is_file:
			s += "SBD: " + str(self.name)
		else:
			s += "TTS: " + str(self.tts)
		
		# Truncate to X characters
		if len(s) > max_length:
			s = s[:max_length] + "..."
		return s

class Playback_Queue:
	q = []

	@staticmethod
	def enqueue(itm):
		L.log(f"Enqueuing {itm.to_str()}", module="Playback_Queue")
		Playback_Queue.q.append(itm)

	@staticmethod
	def dequeue():
		# create a copy of the queue
		itm = Playback_Queue.q[0]
		Playback_Queue.q = Playback_Queue.q[1:]
		L.log(f"Dequeued {itm.to_str()}", module="Playback_Queue")
		return itm
	
	@staticmethod
	def clear():
		L.log(f"Clearing queue", module="Playback_Queue")
		Playback_Queue.q = []

	@staticmethod
	def is_queue_empty():
		return Playback_Queue.q == []

	@staticmethod
	def get_queue_str():
		s = ""
		for itm in Playback_Queue.q:
			s += itm.to_str() + "\n"
		return s

