import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import pygame
from parser import parse_symphony_lang, SymphonyLangParserError
from midi_generator import generate_midi, MIDIGenerationError
from mido import MidiFile

class SymphonyLangGUI:
    def __init__(self, master):
        self.master = master
        master.title("SymphonyLang")
        master.geometry("900x600")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Main frame
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Left frame for input
        left_frame = ttk.Frame(main_frame, width=400)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # Right frame for player and visualization
        right_frame = ttk.Frame(main_frame, width=500)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

        # Text input
        self.input_text = tk.Text(left_frame, wrap=tk.WORD, width=40, height=20)
        self.input_text.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=X)

        compile_button = ttk.Button(button_frame, text="Compile", command=self.compile_code)
        compile_button.pack(side=LEFT, padx=(0, 5))

        upload_button = ttk.Button(button_frame, text="Upload txt", command=self.upload_txt)
        upload_button.pack(side=LEFT)

        # Status message
        self.status_message = ttk.Label(left_frame, text="", wraplength=380)
        self.status_message.pack(fill=X, pady=(10, 0))

        # Music player controls
        self.player_label = ttk.Label(right_frame, text="No MIDI file generated yet")
        self.player_label.pack(pady=20)

        self.play_button = ttk.Button(right_frame, text="Play", command=self.play_midi, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.stop_button = ttk.Button(right_frame, text="Stop", command=self.stop_midi, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Piano visualization canvas
        self.piano_canvas = tk.Canvas(right_frame, width=400, height=150, bg="black")
        self.piano_canvas.pack(pady=10)
        self.draw_piano()  # Draw the static piano keys

        self.midi_file = None
        self.visualization_running = False

    def draw_piano(self):
        """Draws a static piano layout on the canvas with enhanced visuals."""
        key_width = 40
        key_height = 150
        white_keys = 14  # Number of white keys

        # Draw white keys
        for i in range(white_keys):
            self.piano_canvas.create_rectangle(
                i * key_width, 0, (i + 1) * key_width, key_height,
                outline="black", fill="white", width=2  # Enhanced outline
            )

        # Draw black keys
        black_key_positions = [0, 1, 3, 4, 5, 7, 8, 10, 11, 12]
        black_key_width = key_width * 0.6  # Make black keys narrower
        black_key_height = key_height * 0.6

        for i in black_key_positions:
            self.piano_canvas.create_rectangle(
                i * key_width + (key_width - black_key_width) / 2, 0,
                i * key_width + (key_width + black_key_width) / 2, black_key_height,
                outline="black", fill="black", width=2  # Enhanced outline
            )

    def highlight_key(self, note, color="red"):
        """Highlights a key based on MIDI note with better visuals."""
        key_width = 40
        key_height = 150
        black_key_width = key_width * 0.6
        black_key_height = key_height * 0.6
        white_key_positions = [0, 2, 4, 5, 7, 9, 11]  # White keys (C, D, E, F, G, A, B)

        octave = (note // 12) - 1
        key = note % 12

        if key in white_key_positions:  # White key
            position = octave * 7 + white_key_positions.index(key)
            self.piano_canvas.create_rectangle(
                position * key_width, 0, (position + 1) * key_width, key_height,
                outline="black", fill=color, width=2
            )
        else:  # Black key
            black_key_positions = [1, 3, 6, 8, 10]  # Black keys (C#, D#, F#, G#, A#)
            position = octave * 7 + black_key_positions.index(key) if key in black_key_positions else None
            if position is not None:
                self.piano_canvas.create_rectangle(
                    position * key_width + (key_width - black_key_width) / 2, 0,
                    position * key_width + (key_width + black_key_width) / 2, black_key_height,
                    outline="black", fill=color, width=2
                )

    def play_midi(self):
        """Plays the MIDI file and visualizes the keys."""
        if self.midi_file and os.path.exists(self.midi_file):
            try:
                pygame.mixer.music.load(self.midi_file)
                pygame.mixer.music.play()
                self.update_status("Playing MIDI file", "info")
                self.visualize_midi()  # Start visualization
            except pygame.error as e:
                self.update_status(f"Error playing MIDI: {str(e)}", "error")
        else:
            self.update_status("No MIDI file available to play", "warning")

    def visualize_midi(self):
        """Visualizes the MIDI notes on the piano."""
        if not self.midi_file:
            return
        midi = MidiFile(self.midi_file)
        self.visualization_running = True

        for msg in midi.play():
            if not self.visualization_running:
                break
            if msg.type == "note_on" and msg.velocity > 0:
                self.highlight_key(msg.note)
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                self.draw_piano()  # Reset the piano keys
            self.piano_canvas.update()

    def stop_midi(self):
        """Stops MIDI playback and visualization."""
        pygame.mixer.music.stop()
        self.visualization_running = False
        self.draw_piano()  # Reset piano visualization
        self.update_status("Playback stopped", "info")

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
                with open(file_path, "r") as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
                self.update_status(f"File loaded: {os.path.basename(file_path)}", "success")
            except IOError as e:
                self.update_status(f"Error loading file: {str(e)}", "error")

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
