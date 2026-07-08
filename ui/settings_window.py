#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from audio.devices import Audio_Device_Manager
from storage.config_manager import Config_Manager

class Settings:
    def __init__(self, master=None):
        L.log("Initializing Settings Window", module="Settings")

        # other vars
        self.a = Audio_Device_Manager()

        # stringvar for the combo
        self.combo_cv = tk.StringVar()

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
        self.device_combo = ttk.Combobox(self.settings_frame, textvariable=self.combo_cv)
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
        # self.discard_button = ttk.Button(self.settings_control_frame)
        # self.discard_button.configure(text='Discard')
        # self.discard_button.grid(column=2, row=0)
        self.settings_control_frame.pack(side="top")
        frame_7 = ttk.Frame(settings_toplevel)
        frame_7.configure(height=5, width=200)
        frame_7.pack(side="top")

        # bind combobox selected to select_new_odev
        self.device_combo.bind(sequence='<<ComboboxSelected>>', func=self.select_new_odev)

        # Button hookup
        self.save_button.configure(command=self.save_button_action_performed)
        self.device_refresh.configure(command=self.refresh_device_list)

        # Main widget
        self.mainwindow = settings_toplevel

    def run(self):
        L.log("Running Settings Window", module="Settings")

        # setup tasks
        self.populate()

        self.mainwindow.mainloop()

    def populate(self):
        # Get a list of devices from devices.py
        devs = self.a.get_audio_devices()
        o_dev = []
        i_dev = []

        for d in devs:
            l = Audio_Device_Manager.get_in_out(d['index'])
            if(l[0]):
                i_dev.append(d['name'])
            if(l[1]):
                o_dev.append(d['name'])
        
        self.device_combo['values'] = o_dev

    def select_new_odev(self, event):
        L.log("Updating output device...", module="Settings")
        selected_dev = self.device_combo.get()
        L.log(f"Selected device is '{selected_dev}'", module="Settings")

        # Find the deviceid by name
        devs = self.a.get_audio_devices()
        id = -1
        for d in devs:
            if d['name'] == selected_dev:
                id = d['index']
                break
        
        # null check
        if id < 0:
            id = self.a.current_output_device_id
            L.log(f"Selected device not found, using default id of {id}", module="Settings")
        else:
            L.log(f"New device id = {id}", module="Settings")

        # Set the selected device
        L.log("Setting this in the AudioDeviceManager", module="Settings")
        self.a.current_output_device_id = id

        # Save to config
        L.log("Saving to config", module="Settings")
        try:
            Config_Manager.update_config('Output Device', id)
        except KeyError as e:
            L.log(e, level="error", module="Settings")
            return
        L.log("New device id saved", module="Settings")
        
    def refresh_device_list(self):
        L.log("Device refresh button pressed", module="Settings")
        Audio_Device_Manager.get_audio_devices() 
        # Auto-caches this result to Audio_Device_manager.devices, so no need to do anything here
        L.log("Devices refreshed", module="Settings")

    def save_button_action_performed(self):
        L.log("Save button pressed. This does nothing because the software is smart enough to save things by itself, but it makes the user feel good to press it.", module="Settings")
    
if __name__ == "__main__":
    L.setup()
    L.log("settings_window test", module="Settings_Window")
    app = Settings()
    app.run()

