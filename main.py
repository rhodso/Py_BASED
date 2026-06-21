
from logger import L
from audio.audio_engine import Audio_Engine
from ui.main_window import Main_Window

if __name__ == "__main__":
	L.setup()
	L.log("Startup", module="Main")

	# Get the configuration
	from storage.config_manager import Config_Manager
	
	L.log("Loading config", module="Main")
	Config_Manager.set_config_path("config/config.json")
	Config_Manager.load_config()
	L.log(f"Config loaded: {Config_Manager.config}", module="Main")

	L.log("Initialization complete", module="Main")

	app = Main_Window()
	app.run()

