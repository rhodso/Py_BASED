#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # Add parent directory to path
from logger import L

class Soundboard:
    def __init__(self, master=None):
        L.log("Initializing Soundboard Window", module="Soundboard")

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
        button_8 = ttk.Button(self.board_frame)
        button_8.configure(text='button')
        button_8.place(anchor="nw", height=50, width=50, x=0, y=0)
        self.board_frame.pack(anchor="center", side="top")
        self.board_scrollframe.pack(fill="x", side="top")
        self.board_outer_frame.pack(fill="x", side="top")
        self.control_frame = ttk.Frame(self.soundboard_toplevel)
        self.control_frame.configure(height=200, width=200)
        self.add_button = ttk.Button(self.control_frame)
        self.add_button.configure(text='Add')
        self.add_button.grid(column=0, row=0)
        label_2 = ttk.Label(self.control_frame)
        label_2.configure(text='    ')
        label_2.grid(column=1, row=0)
        self.edit_mode_label = ttk.Checkbutton(self.control_frame)
        self.edit_mode_label.configure(text='Edit Mode')
        self.edit_mode_label.grid(column=2, row=0)
        label_3 = ttk.Label(self.control_frame)
        label_3.configure(text='    ')
        label_3.grid(column=4, row=0)
        self.delete_button = ttk.Button(self.control_frame)
        self.delete_button.configure(text='Delete')
        self.delete_button.grid(column=5, row=0)
        self.control_frame.pack(side="top")

        # Main widget
        self.mainwindow = self.soundboard_toplevel

    def run(self):
        L.log("Running Soundboard Window", module="Soundboard")
        self.mainwindow.mainloop()


if __name__ == "__main__":
    L.setup()
    L.log("soundboard_window test", module="Soundboard_Window")
    app = Soundboard()
    app.run()
