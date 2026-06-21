import logging

class L:
	
	@staticmethod
	def setup():
		L.ensure()

		# Log to file
		logging.basicConfig(
			filename="logs/app.log",
			level=logging.DEBUG,
			format="%(asctime)s - %(levelname)s - %(message)s"
		)

	@staticmethod
	def ensure():
		# Ensure logs directory exists
		import os
		if not os.path.exists("logs"):
			os.makedirs("logs")

		# If log file does exist, delete and create a new one
		if os.path.exists("logs/app.log"):
			os.remove("logs/app.log")
		
		with open("logs/app.log", "w") as f:
			f.write("")

	@staticmethod
	def log(msg, level="info", module=None):
		# Format message with module if provided
		msg_string = f"[{module}] {msg}" if module else msg

		if level == "debug":
			logging.debug(msg_string)
		elif level == "warning":
			logging.warning(msg_string)
		elif level == "error":
			logging.error(msg_string)
		else:
			logging.info(msg_string)

