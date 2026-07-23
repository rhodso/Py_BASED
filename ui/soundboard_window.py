#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame
from tkinter import messagebox

import sys
import os

from functools import partial
from threading import Thread

from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L
from storage.soundboard_manager import Soundboard_Manager, Soundboard_Sound
from storage.config_manager import Config_Manager
from audio.audio_engine import Audio_Engine
from ui.soundboard_add_window import Soundboard_Add
from ui.soundboard_del_window import Soundboard_Del
class Soundboard:
    def __init__(self, master=None):
        L.log("Initializing Soundboard Window", module="Soundboard")
        self.edit_mode = False

        # temporarily create 20 sounds:

        # for i in range(30):
        #     t = "Sound " + str(i)
        #     s = Soundboard_Sound()
        #     s.name = t
        #     Soundboard_Manager.sb_btns.append(s)


        Soundboard_Manager.load_sb_btns()

        if isinstance(Config_Manager.config, dict):
            try:    
                cols = Config_Manager.config["Soundboard Columns"]
                if isinstance(cols, int):
                    BUTTONS_PER_ROW = cols
            except KeyError:
                L.log(f"ConfigMangager.config contains no key 'Soundboard Columns'", level="warning", module="Soundboard")

        # build ui
        self.soundboard_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.soundboard_toplevel.configure(height=200, width=200)
        self.soundboard_toplevel.title("BASED-Soundboard")
        self.header_frame = ttk.Frame(self.soundboard_toplevel)
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
        self.search_frame = ttk.Frame(self.soundboard_toplevel)
        self.search_frame.configure(height=200, width=200)
        self.search_label = ttk.Label(self.search_frame)
        self.search_label.configure(font="{Arial} 12 {}", text='Search:')
        self.search_label.pack(side="left")
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.configure(takefocus=True, width=25)
        self.search_entry.pack(side="top")
        self.search_frame.pack(pady=5, side="top")
        separator_1 = ttk.Separator(self.soundboard_toplevel)
        separator_1.configure(orient="horizontal")
        separator_1.pack(fill="x", side="top")
        self.board_outer_frame = ttk.Frame(self.soundboard_toplevel)
        self.board_outer_frame.configure(height=200, width=200)
        self.board_scrollframe = ScrolledFrame(
            self.board_outer_frame, scrolltype="vertical")
        self.board_scrollframe.innerframe.configure(width=250)
        self.board_scrollframe.configure(usemousewheel=True)
        self.board_frame = ttk.Frame(self.board_scrollframe.innerframe)
        self.board_frame.configure(height=200, width=250)
        
        self.sb_buttons = []
        self.button_images = []

        # Start of dynamic ui code

        self.rebuild_soundboard()

        # End of dynamic ui code

        self.board_frame.pack(anchor="center", side="top")
        self.board_scrollframe.pack(fill="x", side="top")
        self.board_outer_frame.pack(fill="x", side="top")
        self.control_frame = ttk.Frame(self.soundboard_toplevel)
        self.control_frame.configure(height=200, width=200)
        self.add_button = ttk.Button(self.control_frame)
        self.add_button.configure(text='Add')
        self.add_button.grid(column=0, row=0)
        self.add_button.config(command=self.add_sb_entry)
        label_2 = ttk.Label(self.control_frame)
        label_2.configure(text='    ')
        label_2.grid(column=1, row=0)
        self.edit_mode_tickbox = ttk.Checkbutton(self.control_frame, text='Edit Mode', onvalue=1, offvalue=0)
        self.edit_mode_tickbox.config(command=self.on_edit_toggle)
        self.edit_mode_tickbox.state(["!alternate"])
        self.edit_mode_tickbox.grid(column=2, row=0)
        label_3 = ttk.Label(self.control_frame)
        label_3.configure(text='    ')
        label_3.grid(column=4, row=0)
        self.delete_button = ttk.Button(self.control_frame)
        self.delete_button.configure(text='Delete')
        self.delete_button.grid(column=5, row=0)
        self.delete_button.config(command=self.delete_sb_sound)
        self.control_frame.pack(side="top")

        # Main widget
        self.mainwindow = self.soundboard_toplevel



    def rebuild_soundboard(self):
        L.log(f"Redrawing Button UI", module="Soundboard")
        BUTTON_SIZE = 50
        BUTTON_PADDING = 2
        BUTTONS_PER_ROW = 5

        # Clear existing widgets
        for btn in self.sb_buttons:
            btn.destroy()

        self.sb_buttons.clear()
        self.button_images.clear()

        # Reload file
        Soundboard_Manager.load_sb_btns()

        # Rebuild buttons
        for i, sound in enumerate(Soundboard_Manager.sb_btns):
            if not isinstance(sound, Soundboard_Sound):
                continue

            x = (i % BUTTONS_PER_ROW) * (BUTTON_SIZE + BUTTON_PADDING)
            y = (i // BUTTONS_PER_ROW) * (BUTTON_SIZE + BUTTON_PADDING)

            btn = ttk.Button(
                self.board_frame,
                command=partial(self.sb_button_action, sound)
            )

            if not sound.icon_fp:
                btn.configure(text=sound.name)
            else:
                image = Image.open(sound.icon_fp).convert("RGBA")
                image.thumbnail((BUTTON_SIZE, BUTTON_SIZE), Image.Resampling.LANCZOS)

                canvas = Image.new("RGBA", (BUTTON_SIZE, BUTTON_SIZE), (0, 0, 0, 0))
                canvas.paste(
                    image,
                    (
                        (BUTTON_SIZE-image.width)//2,
                        (BUTTON_SIZE-image.height)//2
                    ),
                    image
                )

                photo = ImageTk.PhotoImage(canvas)

                # IMPORTANT: keep a reference
                self.button_images.append(photo)

                btn.configure(image=photo)

            btn.place(
                x=x,
                y=y,
                width=BUTTON_SIZE,
                height=BUTTON_SIZE
            )

            self.sb_buttons.append(btn)

        rows = (len(self.sb_buttons) + BUTTONS_PER_ROW - 1) // BUTTONS_PER_ROW
        width = BUTTONS_PER_ROW * (BUTTON_SIZE + BUTTON_PADDING) - BUTTON_PADDING
        height = rows * (BUTTON_SIZE + BUTTON_PADDING) - BUTTON_PADDING

        self.board_frame.configure(width=width, height=height)
        

    def add_sb_entry(self):
        L.log(f"Adding new SB entry","Soundboard")
        s = Soundboard_Add()
        # Add ref to this so we can tell the add window to redraw the ui
        # This is a bad way of doing this, but it works for now
        s.add_ref(self)  
        s.run()

        # Redraw the UI
        L.log(f"Redrawing UI from SB add","Soundboard")
        self.rebuild_soundboard()

    def delete_sb_sound(self):
        # Create a popup with what sounds to delete
        opts = []
        for sound in Soundboard_Manager.sb_btns:
            opts.append(sound.name)

        s = Soundboard_Del(combo_vals=opts)
        s.add_ref(self)
        s.run()

        # Redraw the UI
        L.log(f"Redrawing UI from SB del","Soundboard")
        self.rebuild_soundboard()

    def run(self):
        L.log("Running Soundboard Window", module="Soundboard")
        self.mainwindow.mainloop()

    def on_edit_toggle(self):
        self.edit_mode = self.edit_mode_tickbox.instate(["selected"])
        L.log(f"Edit mode state is now: {self.edit_mode}", module="Soundboard")
   
    def sb_button_action(self, sound: Soundboard_Sound):
        L.log(f"Soundboard button pressed '{sound.name}', editmode = {self.edit_mode}", module="Soundboard")

        if self.edit_mode:
            messagebox.showwarning("Not Implimented", "Edit mode not yet implimented. Untick the box to play sounds normally")
        else:        
            if(sound.is_file):
                L.log(f"Sound is a file, playing file", module="Soundboard")
                thread = Thread(target=Audio_Engine.play_file(sound.fp))
                thread.start()
                thread.join()

            else:
                L.log(f"Sound is pre-saved tts, sending to tts", module="Soundboard")
                thread = Thread(target=Audio_Engine.play_text(sound.tts))
                thread.start()
                thread.join()

if __name__ == "__main__":
    L.setup()
    L.log("soundboard_window test", module="Soundboard_Window")

    Config_Manager.load_config()

    app = Soundboard()
    app.run()

