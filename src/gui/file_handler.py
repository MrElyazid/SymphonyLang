import tkinter as tk
from tkinter import filedialog
import os
from parser import parse_symphony_lang, SymphonyLangParserError
from midi_generator import generate_midi, MIDIGenerationError

class FileHandler:
    def __init__(self, text_widget, status_callback, set_midi_file_callback, enable_controls_callback):
        self.input_text = text_widget
        self.update_status = status_callback
        self.set_midi_file = set_midi_file_callback
        self.enable_controls = enable_controls_callback

    def compile_code(self):
        """Compiles the SymphonyLang code to MIDI."""
        code = self.input_text.get("1.0", tk.END).strip()
        try:
            parsed_composition = parse_symphony_lang(code)
            midi_file = "output.mid"
            generate_midi(parsed_composition, midi_file)
            self.set_midi_file(midi_file)
            self.enable_controls(True)
            self.update_status("MIDI file generated successfully!", "success")
        except (SymphonyLangParserError, MIDIGenerationError) as e:
            self.update_status(f"Error: {str(e)}", "error")
            self.enable_controls(False)

    def upload_txt(self):
        """Handles text file upload."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
                self.update_status(f"File loaded: {os.path.basename(file_path)}", "success")
            except IOError as e:
                self.update_status(f"Error loading file: {str(e)}", "error")
