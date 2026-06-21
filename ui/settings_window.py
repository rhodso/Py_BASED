#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L

class Settings:
    def __init__(self, master=None):
        L.log("Initializing Settings Window", module="Settings")

        # build ui
        settings_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        settings_toplevel.configure(height=200, width=200)
        self.header_frame = ttk.Frame(settings_toplevel)
        self.header_frame.configure(height=200, width=200)
        self.header_label = ttk.Label(self.header_frame)
        self.header_label.configure(font="{Arial} 12 {bold}", text='BASED')
        self.header_label.pack(side="top")
        self.caption_label = ttk.Label(self.header_frame)
        self.caption_label.configure(
            font="{Arial} 7 {italic}",
            text='Broadcast Automation System for Electronic Devices')
        self.caption_label.pack(side="top")
        self.header_frame.pack(side="top")
        frame_5 = ttk.Frame(settings_toplevel)
        frame_5.configure(height=10, width=200)
        frame_5.pack(side="top")
        self.settings_frame = ttk.Frame(settings_toplevel)
        self.settings_frame.configure(height=200, width=200)
        self.device_selection_label = ttk.Label(self.settings_frame)
        self.device_selection_label.configure(
            justify="center", text='Device\nSelection')
        self.device_selection_label.grid(column=0, row=0)
        self.device_combo = ttk.Combobox(self.settings_frame)
        self.device_combo.grid(column=1, row=0)
        self.device_refresh = ttk.Button(self.settings_frame)
        self.device_refresh.configure(text='R', width=2)
        self.device_refresh.grid(column=2, row=0)
        self.sb_cols_label = ttk.Label(self.settings_frame)
        self.sb_cols_label.configure(
            justify="center", text='Soundboard\nColumns')
        self.sb_cols_label.grid(column=0, row=1)
        self.sb_cols_entry = ttk.Entry(self.settings_frame)
        self.sb_cols_entry.configure(width=25)
        self.sb_cols_entry.grid(column=1, columnspan=2, row=1)
        self.settings_frame.pack(side="top")
        frame_3 = ttk.Frame(settings_toplevel)
        frame_3.configure(height=10, width=200)
        frame_3.pack(side="top")
        self.settings_control_frame = ttk.Frame(settings_toplevel)
        self.settings_control_frame.configure(height=200, width=200)
        self.save_button = ttk.Button(self.settings_control_frame)
        self.save_button.configure(text='Save')
        self.save_button.grid(column=0, row=0)
        label_3 = ttk.Label(self.settings_control_frame)
        label_3.configure(text='            ')
        label_3.grid(column=1, row=0)
        self.discard_button = ttk.Button(self.settings_control_frame)
        self.discard_button.configure(text='Discard')
        self.discard_button.grid(column=2, row=0)
        self.settings_control_frame.pack(side="top")
        frame_7 = ttk.Frame(settings_toplevel)
        frame_7.configure(height=5, width=200)
        frame_7.pack(side="top")

        # Main widget
        self.mainwindow = settings_toplevel

    def run(self):
        L.log("Running Settings Window", module="Settings")
        self.mainwindow.mainloop()


if __name__ == "__main__":
    L.setup()
    L.log("settings_window test", module="Settings_Window")
    app = Settings()
    app.run()
