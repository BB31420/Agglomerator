import tkinter as tk
import customtkinter as ctk
import os
import subprocess
from tkinter import filedialog
import tempfile
from tkinter import messagebox
import ffmpy
import shlex
from pathlib import Path
from ffmpy import FFprobe
import re
from video_utils import combine_videos

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class VideoCombiner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.title("Agglomerator")
        self.geometry("700x600")
        self.configure(padx=10, pady=10)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=False)
        self.file_listbox.grid(row=0, column=0, columnspan=5, sticky="nsew")

        self.add_file_button = ctk.CTkButton(self, text="Add Video File", command=self.add_file)
        self.add_file_button.grid(row=1, column=0, sticky="nsew")

        self.remove_file_button = ctk.CTkButton(self, text="Remove Video File", command=self.remove_file)
        self.remove_file_button.grid(row=1, column=1, sticky="nsew")

        self.move_up_button = ctk.CTkButton(self, text="Move Up", command=lambda: self.move_file(-1))
        self.move_up_button.grid(row=1, column=2, sticky="nsew")

        self.move_down_button = ctk.CTkButton(self, text="Move Down", command=lambda: self.move_file(1))
        self.move_down_button.grid(row=1, column=3, sticky="nsew")

        self.combine_button = ctk.CTkButton(self, text="Combine Videos", command=self.combine_videos)
        self.combine_button.grid(row=1, column=4, sticky="nsew")

        for i in range(5):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(1, weight=0)

    def add_file(self):
        file_paths = filedialog.askopenfilenames(multiple=True)
        if file_paths:
            for file_path in file_paths:
                self.file_listbox.insert(tk.END, file_path)


    def remove_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            self.file_listbox.delete(selected_index)

    def move_file(self, direction):
        selected_index = self.file_listbox.curselection()
        if selected_index and 0 <= selected_index[0] + direction < self.file_listbox.size():
            self.file_listbox.insert(selected_index[0] + direction, self.file_listbox.get(selected_index))
            self.file_listbox.delete(selected_index[0])
            self.file_listbox.select_set(selected_index[0] + direction)

    def combine_videos(self):
        file_paths = self.file_listbox.get(0, tk.END)
        output_file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])
        if not output_file_path:
            return

        combine_videos(file_paths, output_file_path)

        messagebox.showinfo("Success", "Video files combined successfully.")


if __name__ == "__main__":
    app = VideoCombiner()
    app.mainloop()