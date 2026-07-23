#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from storage.soundboard_manager import Soundboard_Manager

class Soundboard_Del:
	def __init__(self, master=None, combo_vals = []):
		L.log(f"Creating SB Remove dialogue with {len(combo_vals)} options", module="Soundboard_Delete")

		# build ui
		self.delpopup_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
		self.delpopup_toplevel.configure(height=200, width=200)
		self.delpopup_main_frame = ttk.Frame(self.delpopup_toplevel)
		self.delpopup_main_frame.configure(height=200, width=200)
		self.delpopup_header_frame = ttk.Frame(self.delpopup_main_frame)
		self.delpopup_header_frame.configure(height=200, width=200)
		self.delpopup_header_label = ttk.Label(self.delpopup_header_frame)
		self.delpopup_header_label.configure(text='Select item to delete:')
		self.delpopup_header_label.pack(side="top")
		self.delpopup_header_frame.pack(side="top")
		self.delpopup_comboframe = ttk.Frame(self.delpopup_main_frame)
		self.delpopup_comboframe.configure(height=200, width=200)
		self.delpopup_combo = ttk.Combobox(self.delpopup_comboframe)
		self.delpopup_combo['values'] = combo_vals		
		self.delpopup_combo.pack(side="top")
		self.delpopup_comboframe.pack(side="top")
		self.delpopup_button_frame = ttk.Frame(self.delpopup_main_frame)
		self.delpopup_button_frame.configure(height=200, width=200)
		self.delpopup_delete_button = ttk.Button(self.delpopup_button_frame)
		self.delpopup_delete_button.configure(text='Delete')
		self.delpopup_delete_button.config(command=self.del_sb)
		self.delpopup_delete_button.grid(column=0, row=0)
		self.delpopup_spacer_label = ttk.Label(self.delpopup_button_frame)
		self.delpopup_spacer_label.configure(text='		 ')
		self.delpopup_spacer_label.grid(column=1, row=0)
		self.delpopup_cancel_button = ttk.Button(self.delpopup_button_frame)
		self.delpopup_cancel_button.configure(text='Cancel')
		self.delpopup_cancel_button.config(command=self.cancel_sb)
		self.delpopup_cancel_button.grid(column=2, row=0)
		self.delpopup_button_frame.pack(side="top")
		self.delpopup_main_frame.pack(side="top")

		# Main widget
		self.mainwindow = self.delpopup_toplevel
		self.delpopup_combo.current(1)

	def run(self):
		self.mainwindow.mainloop()

	def add_ref(self, ref):
		self.ref = ref

	def del_sb(self):
		# Get the value of the combobox
		v = self.delpopup_combo.get()
		L.log(f"Removing sound {v} from Soundboard", module="Soundboard_Delete")

		if v == "":
			return

		for sound in Soundboard_Manager.sb_btns:
			if sound.name == v:
				Soundboard_Manager.sb_btns.remove(sound)
				break

		L.log(f"Removed sound", module="Soundboard_Delete")
		Soundboard_Manager.save_sb_btns()
		L.log(f"Saved SB file", module="Soundboard_Delete")
		self.close_window()

	def cancel_sb(self):
		self.close_window()

	def close_window(self):
		# Tell the main soundboard window to redraw the ui
		self.ref.rebuild_soundboard()
		self.mainwindow.destroy()

