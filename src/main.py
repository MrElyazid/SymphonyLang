import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import pygame
from parser import parse_symphony_lang, SymphonyLangParserError
from midi_generator import generate_midi, MIDIGenerationError

class SymphonyLangGUI:
    def __init__(self, master):
        self.master = master
        master.title("SymphonyLang")
        master.geometry("800x600")

        # pygame mixer an7tajoh bach nkhadmo audio file b pygame
        pygame.mixer.init()

        # main frame if fih other frames
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # frame dyal input
        left_frame = ttk.Frame(main_frame, width=400)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # right frame dyal audio player
        right_frame = ttk.Frame(main_frame, width=400)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        # text input il kin f right frame
        self.input_text = tk.Text(left_frame, wrap=tk.WORD, width=40, height=20)
        self.input_text.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=X)

        compile_button = ttk.Button(button_frame, text="Compile", command=self.compile_code)
        compile_button.pack(side=LEFT, padx=(0, 5))

        upload_button = ttk.Button(button_frame, text="Upload txt", command=self.upload_txt)
        upload_button.pack(side=LEFT)

        # status message, wach comiling sucessful, with errors ... etc
        self.status_message = ttk.Label(left_frame, text="", wraplength=380)
        self.status_message.pack(fill=X, pady=(10, 0))

        # music player controls
        self.player_label = ttk.Label(right_frame, text="No MIDI file generated yet")
        self.player_label.pack(pady=20)

        self.play_button = ttk.Button(right_frame, text="Play", command=self.play_midi, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.stop_button = ttk.Button(right_frame, text="Stop", command=self.stop_midi, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.midi_file = None

    def compile_code(self):
        code = self.input_text.get("1.0", tk.END).strip()
        try:
            parsed_composition = parse_symphony_lang(code)
            self.midi_file = "output.mid"
            generate_midi(parsed_composition, self.midi_file)
            self.player_label.config(text="MIDI file generated: output.mid")
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.update_status("MIDI file generated successfully!", "success")
        except (SymphonyLangParserError, MIDIGenerationError) as e:
            self.update_status(f"Error: {str(e)}", "error")
            self.midi_file = None
            self.play_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

    def upload_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
                self.update_status(f"File loaded: {os.path.basename(file_path)}", "success")
            except IOError as e:
                self.update_status(f"Error loading file: {str(e)}", "error")

    def play_midi(self):
        if self.midi_file and os.path.exists(self.midi_file):
            try:
                pygame.mixer.music.load(self.midi_file)
                pygame.mixer.music.play()
                self.update_status("Playing MIDI file", "info")
            except pygame.error as e:
                self.update_status(f"Error playing MIDI: {str(e)}", "error")
        else:
            self.update_status("No MIDI file available to play", "warning")

    def stop_midi(self):
        pygame.mixer.music.stop()
        self.update_status("Playback stopped", "info")

    def update_status(self, message, status_type):
        self.status_message.config(text=message)
        if status_type == "error":
            self.status_message.config(foreground="red")
        elif status_type == "success":
            self.status_message.config(foreground="green")
        elif status_type == "warning":
            self.status_message.config(foreground="orange")
        else:
            self.status_message.config(foreground="white")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    gui = SymphonyLangGUI(root)
    root.mainloop()