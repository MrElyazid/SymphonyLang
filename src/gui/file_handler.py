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
        self.pseudo_code_snippets = [
            """
tempo=120

# Play a simple melody
C4 qn
E4 qn
G4 hn
C5 wn

# Add a scale
C4 maj
""",
            """
tempo=100

# Play a different melody
D4 qn
F#4 qn
A4 hn
D5 wn

# Add a scale
D4 min
""",
            """
tempo=140

# Play a new melody
E4 qn
G#4 qn
B4 hn
E5 wn

# Add a scale
E4 maj
""",
        
        ]
        self.current_snippet_index = 0

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

    def generate_pseudo_code(self):
        """Generates pseudo code for testing."""
        pseudo_code = self.pseudo_code_snippets[self.current_snippet_index]
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, pseudo_code)
        self.update_status("Pseudo code generated!", "success")
        
        self.current_snippet_index = (self.current_snippet_index + 1) % len(self.pseudo_code_snippets)
