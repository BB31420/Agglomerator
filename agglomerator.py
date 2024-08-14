import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk
import os
from pathlib import Path
from video_utils import VideoProcessor

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class VideoCombiner(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.title("Agglomerator")
        self.geometry("800x600")
        self.configure(padx=20, pady=20)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=False, font=("Roboto Condensed", 12))
        self.file_listbox.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        self.add_file_button = ctk.CTkButton(button_frame, text="Add Video Files", command=self.add_files)
        self.add_file_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.remove_file_button = ctk.CTkButton(button_frame, text="Remove Video File", command=self.remove_file)
        self.remove_file_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.move_up_button = ctk.CTkButton(button_frame, text="Move Up", command=lambda: self.move_file(-1))
        self.move_up_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.move_down_button = ctk.CTkButton(button_frame, text="Move Down", command=lambda: self.move_file(1))
        self.move_down_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.combine_button = ctk.CTkButton(self, text="Combine Videos", command=self.combine_videos)
        self.combine_button.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

    def add_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
        if file_paths:
            for file_path in file_paths:
                try:
                    # Attempt to get the absolute path
                    abs_path = os.path.abspath(file_path)
                    # Check if the file exists and is readable
                    if os.path.exists(abs_path) and os.access(abs_path, os.R_OK):
                        truncated_name = self.truncate_filename(os.path.basename(abs_path))
                        self.file_listbox.insert(tk.END, f"{truncated_name} ({abs_path})")
                    else:
                        messagebox.showwarning("File Access Error", f"Unable to access file: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error adding file {file_path}: {str(e)}")

    def truncate_filename(self, filename, max_length=40):
        if len(filename) <= max_length:
            return filename
        return filename[:max_length-3] + "..."

    def remove_file(self):
        if self.file_listbox.size() == 0:
            return

        selected_index = self.file_listbox.curselection()
        if selected_index:
            self.file_listbox.delete(selected_index)
            # Select the next item or the last item if we deleted the last one
            next_index = selected_index[0]
            if next_index >= self.file_listbox.size():
                next_index = self.file_listbox.size() - 1
            if next_index >= 0:
                self.file_listbox.select_set(next_index)
        else:
            # If nothing is selected, remove the first item
            self.file_listbox.delete(0)
            if self.file_listbox.size() > 0:
                self.file_listbox.select_set(0)

    def move_file(self, direction):
        selected_index = self.file_listbox.curselection()
        if selected_index and 0 <= selected_index[0] + direction < self.file_listbox.size():
            selected_item = self.file_listbox.get(selected_index)
            self.file_listbox.delete(selected_index)
            new_index = selected_index[0] + direction
            self.file_listbox.insert(new_index, selected_item)
            self.file_listbox.select_set(new_index)

    def combine_videos(self):
        file_paths = [item.split(" (")[-1][:-1] for item in self.file_listbox.get(0, tk.END)]
        if not file_paths:
            messagebox.showwarning("Warning", "Please add video files before combining.")
            return

        output_file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])
        if not output_file_path:
            return

        result = VideoProcessor.combine_videos(file_paths, output_file_path)

        if result:
            messagebox.showinfo("Success", "Video files combined successfully.")
        else:
            messagebox.showerror("Error", "Failed to combine video files.")

if __name__ == "__main__":
    app = VideoCombiner()
    app.mainloop()
