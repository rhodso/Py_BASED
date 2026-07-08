#!/usr/bin/python3

from threading import Thread

import tkinter as tk
import tkinter.ttk as ttk

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from audio.audio_engine import Audio_Engine

from ui.soundboard_window import Soundboard
from ui.settings_window import Settings

#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk

class Main_Window:
    def __init__(self, master=None):
        # build ui
        toplevel_1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel_1.configure(height=200, width=200)
        toplevel_1.title("BASED-MainWindow")
        self.header_frame = ttk.Frame(toplevel_1)
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
        self.tts_frame = ttk.Frame(toplevel_1)
        self.tts_frame.configure(height=200, width=200)
        self.tts_input = tk.Text(self.tts_frame)
        self.tts_input.configure(
            cursor="arrow",
            font="TkDefaultFont",
            height=3,
            undo=True,
            width=38,
            wrap="word")
        _text_ = 'TTS'
        self.tts_input.insert("0.0", _text_)
        self.tts_input.pack(side="top")
        self.tts_control_frame = ttk.Frame(self.tts_frame)
        self.tts_control_frame.configure(height=200, width=200)
        self.speak_button = ttk.Button(self.tts_control_frame)
        self.speak_button.configure(text='Speak')
        self.speak_button.grid(column=0, row=0)
        self.speak_button.configure(command=self.speak_button_action)
        self.stop_button = ttk.Button(self.tts_control_frame)
        self.stop_button.configure(text='Stop')
        self.stop_button.grid(column=1, row=0)
        self.stop_button.configure(command=self.stop_button_action)
        self.clear_queue_button = ttk.Button(self.tts_control_frame)
        self.clear_queue_button.configure(text='Clear Queue')
        self.clear_queue_button.grid(column=2, row=0)
        self.clear_queue_button.configure(
            command=self.clearqueue_button_action)
        self.tts_control_frame.pack(side="top")
        self.tts_frame.pack(side="top")
        self.queue_frame = ttk.Frame(toplevel_1)
        self.queue_frame.configure(height=200, width=200)
        self.queue_text = tk.Text(self.queue_frame)
        self.queue_text.configure(exportselection=True, height=3, width=30)
        self.queue_text.pack(side="top")
        self.queue_frame.pack(side="top")
        self.button_frame = ttk.Frame(toplevel_1)
        self.button_frame.configure(height=200, width=200)
        self.open_soundboard_button = ttk.Button(self.button_frame)
        self.open_soundboard_button.configure(text='Soundboard')
        self.open_soundboard_button.grid(column=0, row=0)
        self.open_soundboard_button.configure(
            command=self.open_soundborard_action)
        self.settings_button = ttk.Button(self.button_frame)
        self.settings_button.configure(text='Settings')
        self.settings_button.grid(column=2, row=0)
        self.settings_button.configure(command=self.open_settings_action)
        label_3 = ttk.Label(self.button_frame)
        label_3.configure(text='                  ')
        label_3.grid(column=1, row=0)
        self.button_frame.pack(side="top")
        self.spacer_frame = ttk.Frame(toplevel_1)
        self.spacer_frame.configure(height=10, width=200)
        self.spacer_frame.pack(side="top")
        self.status_frame = ttk.Frame(toplevel_1)
        self.status_frame.configure(height=200, width=200)
        self.status_header = ttk.Label(self.status_frame)
        self.status_header.configure(font="{Arial} 12 {}", text='Status:')
        self.status_header.grid(column=0, row=0)
        self.status_label = ttk.Label(self.status_frame)
        self.status_label.configure(
            font="{Arial} 12 {}",
            text='Loading Application',
            width=20)
        self.status_label.grid(column=1, row=0)
        self.status_frame.pack(side="top")

        # Main widget
        self.mainwindow = toplevel_1

    def run(self):
        self.status_label.config(text = "Ready")
        self.mainwindow.mainloop()

    def speak_button_action(self):
        self.status_label.config(text = "Getting text")
        t = self.tts_input.get("1.0", "end-1c")
        self.status_label.config(text = "Playing audio")
        thread = Thread(target=Audio_Engine.play_text(t))
        thread.start()
        thread.join()
        self.status_label.config(text = "Ready")

    def stop_button_action(self):
        Audio_Engine.stop()

    def clearqueue_button_action(self):
        pass

    def open_soundborard_action(self):
        self.sbd = Soundboard()
        self.sbd.run()

    def open_settings_action(self):
        self.stt = Settings()
        self.stt.run()

