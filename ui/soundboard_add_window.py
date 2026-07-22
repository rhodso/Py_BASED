#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

from pygubu.widgets.pathchooserinput import PathChooserInput

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from storage.soundboard_manager import Soundboard_Manager

class Soundboard_Add:
	def __init__(self, master=None):
		# build ui
		toplevel_1 = tk.Tk() if master is None else tk.Toplevel(master)
		toplevel_1.configure(height=200, width=250)
		self.header_frame = ttk.Frame(toplevel_1)
		self.header_frame.configure(height=200, width=250)
		self.header_label = ttk.Label(self.header_frame)
		self.header_label.configure(font="{Arial} 12 {bold}", text='BASED')
		self.header_label.pack(side="top")
		self.caption_label = ttk.Label(self.header_frame)
		self.caption_label.configure(
			font="{Arial} 7 {italic}",
			text='Broadcast Automation System for Electronic Devices')
		self.caption_label.pack(side="top")
		self.header_frame.pack(expand=True, fill="x", side="top")
		frame_1 = ttk.Frame(toplevel_1)
		frame_1.configure(height=200, width=250)
		label_1 = ttk.Label(frame_1)
		label_1.configure(
			font="{Arial} 12 {}",
			text='Add New Soundboard Button')
		label_1.pack(side="top")
		separator_1 = ttk.Separator(frame_1)
		separator_1.configure(orient="horizontal")
		separator_1.pack(expand=False, fill="x", side="top")
		frame_2 = ttk.Frame(frame_1)
		frame_2.configure(height=200, width=250)
		self.name_label = ttk.Label(frame_2)
		self.name_label.configure(text='Sound Name')
		self.name_label.grid(column=0, row=0)
		self.name_entry = ttk.Entry(frame_2)
		self.name_entry.configure(width=26)
		self.name_entry.grid(column=1, columnspan=2, row=0)
		self.imagefp_name_label = ttk.Label(frame_2)
		self.imagefp_name_label.configure(
			compound="top", font="TkMenuFont", text='Image FP')
		self.imagefp_name_label.grid(column=0, row=1)
		self.imagefp_chooser = PathChooserInput(frame_2)
		self.imagefp_chooser.configure(mustexist=True, type="file")
		self.imagefp_chooser.grid(column=1, row=1)
		labelframe_2 = ttk.Labelframe(frame_2)
		labelframe_2.configure(
			height=200,
			text='TTS Soundboard Entry',
			width=250)
		label_5 = ttk.Label(labelframe_2)
		label_5.configure(text='TTS Text')
		label_5.grid(column=0, row=0)
		self.tts_text_entry = ttk.Entry(labelframe_2)
		self.tts_text_entry.configure(width=20)
		self.tts_text_entry.grid(column=1, columnspan=2, row=0)
		labelframe_2.grid(column=0, columnspan=3, row=3)
		labelframe_2.columnconfigure(0, minsize=130, pad=5)
		labelframe_3 = ttk.Labelframe(frame_2)
		labelframe_3.configure(
			height=200,
			text='File Soundboard Entry',
			width=200)
		label_6 = ttk.Label(labelframe_3)
		label_6.configure(text='SB Filepath')
		label_6.grid(column=0, row=0)
		self.fp_chooser = PathChooserInput(labelframe_3)
		self.fp_chooser.configure(mustexist=True, type="file")
		self.fp_chooser.grid(column=1, row=0)
		labelframe_3.grid(column=0, columnspan=3, row=4)
		labelframe_3.columnconfigure(0, minsize=90, pad=5)
		frame_2.pack(side="top")
		frame_1.pack(side="top")
		frame_4 = ttk.Frame(toplevel_1)
		frame_4.configure(height=200, width=250)
		self.cancel_button = ttk.Button(frame_4)
		self.cancel_button.configure(text='Cancel')
		self.cancel_button.grid(column=0, row=0)
		self.cancel_button.configure(command=self.cancel_button_action)
		label_2 = ttk.Label(frame_4)
		label_2.configure(text='				   ')
		label_2.grid(column=1, row=0)
		button_2 = ttk.Button(frame_4)
		button_2.configure(text='Add')
		button_2.grid(column=2, row=0)
		button_2.configure(command=self.add_button_action)
		frame_4.pack(side="top")

		# Main widget
		self.mainwindow = toplevel_1

	def run(self):
		L.log(f"Building UI to add new SB button",module="Soundboard_Add")
		self.mainwindow.mainloop()

	def add_ref(self, ref):
		self.ref = ref

	def cancel_button_action(self):
		L.log(f"New SB button cancelled",module="Soundboard_Add")
		self.close_window()

	def add_button_action(self):
		L.log(f"Adding new soundboard button",module="Soundboard_Add")

		# Add to dictionary
		d = {
			"name": self.name_entry.get(),
			"fp": self.fp_chooser.cget('path'),
			"tts_text": self.tts_text_entry.get(),
			"icon_fp": self.imagefp_chooser.cget('path'),
			"vol": 1.0
		}

		# Determine if file or not file
		# If there is a file path, then it's a file, since this requires more effort
		d["is_file"] = d["fp"] != ""

		# Validate
		is_valid = self.validate(d)
		if(not is_valid):
			return
		
		# New SBB is valid, add to SB
		Soundboard_Manager.add_sb_btn(d)

		# Close window
		self.close_window()
	
	def close_window(self):
		# Tell the main soundboard window to redraw the ui
		self.ref.rebuild_soundboard()
		self.mainwindow.destroy()

	def validate(self, d):
		L.log(f"Validating new SB ({d})",module="Soundboard_Add")
		# Ensure that name and either path or text are set
		if d["name"] == "":
			L.log(f"New soundboard sound name not set, cannot continue", module="Soundboard_Add", level="error")
			messagebox.showerror("Error", "Name must be set to save sound")
			return False
		if (d["fp"] == "") and (d["tts_text"] == ""):
			L.log(f"New soundboard sound fp or tts_text not set, cannot continue", module="Soundboard_Add", level="error")
			messagebox.showerror("Error", "Either sound filepath or tts text must be set to save sound")
			return False
		
		# Check path exists
		if(d["fp"] != ""):
			if(not os.path.exists(d["fp"])):
				L.log(f"Filepath {d['fp']} does not exist", module="Soundboard_Add", level="error")
				messagebox.showerror("Error", "Provided sound filepath does not exist")
				return False
		
		# Check image path exists if provided
		if(d["icon_fp"] != ""):
			if(not os.path.exists(d["icon_fp"])):
				L.log(f"Provided sound icon file {d['fp']} does not exist", module="Soundboard_Add", level="error")
				messagebox.showerror("Error", "Provided image fp does not exist")

		# TODO: Think of other checks to add here

		return True

if __name__ == "__main__":
	app = Soundboard_Add()
	app.run()
