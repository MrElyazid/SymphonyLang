import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import pygame
from parser import parse_symphony_lang, SymphonyLangParserError
from midi_generator import generate_midi, MIDIGenerationError
from mido import MidiFile
import random

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

        # Bar chart-like visualization canvas
        self.visualization_canvas = tk.Canvas(right_frame, width=500, height=200, bg="white")
        self.visualization_canvas.pack(pady=10)

        self.midi_file = None
        self.visualization_running = False
        self.note_positions = []  # Store positions of notes for visualization

    def draw_bar_chart(self):
        """Draws a more elegant bar chart with smooth transitions."""
        self.visualization_canvas.delete("all")  # Clear previous drawing
        if not self.note_positions:
            return

        # Set a bar width and horizontal separation
        bar_width = 25
        bar_gap = 30  # Gap between bars
        x_offset = 10  # Horizontal offset to separate bars

        # Note duration to height mapping
        note_heights = {
            "wn": 180,  # Whole note
            "hn": 140,  # Half note
            "qn": 100,  # Quarter note
            "en": 70,   # Eighth note
            "sn": 50    # Sixteenth note
        }

        for time, pitch, duration in self.note_positions:
            # Set the height based on the note duration
            height = note_heights.get(duration, 50)  # Default height if unknown
            x1 = x_offset
            y1 = 200 - height  # Invert the height for visualization
            x2 = x1 + bar_width
            y2 = 200

            # Generate a random pastel color for each bar
            color = self.get_random_pastel_color()

            # Draw the bar with a smooth transition effect (growing bar)
            self.visualization_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

            # Add a label with the note duration
            self.visualization_canvas.create_text((x1 + x2) / 2, y1 - 10, text=duration, fill="black", font=("Helvetica", 8))

            # Update the x_offset for the next bar
            x_offset = x2 + bar_gap

    def get_random_pastel_color(self):
        """Generates a random pastel color."""
        r = random.randint(200, 255)
        g = random.randint(200, 255)
        b = random.randint(200, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def play_midi(self):
        """Plays the MIDI file and visualizes the notes."""
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
        """Visualizes the MIDI notes on the bar chart."""
        if not self.midi_file:
            return
        midi = MidiFile(self.midi_file)
        self.visualization_running = True

        # Iterate over MIDI messages and track note positions for the graph
        for msg in midi.play():
            if not self.visualization_running:
                break
            if msg.type == "note_on" and msg.velocity > 0:
                # Store the time, pitch, and note duration for visualization
                note_duration = self.get_note_duration(msg.note)
                self.note_positions.append((msg.time * 10, msg.note, note_duration))  # Example scaling
                self.draw_bar_chart()  # Update the bar chart
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                self.note_positions.append((msg.time * 10, 200, "sn"))  # Reset position on note off
                self.draw_bar_chart()  # Update the bar chart
            self.visualization_canvas.update()

    def stop_midi(self):
        """Stops MIDI playback and visualization."""
        pygame.mixer.music.stop()
        self.visualization_running = False
        self.note_positions.clear()  # Clear previous note positions
        self.visualization_canvas.delete("all")  # Clear the canvas
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

    def get_note_duration(self, pitch):
        """Determines the note duration based on pitch or other criteria."""
        # Example logic for note duration (this can be adapted)
        if pitch > 72:  # Whole note
            return "wn"
        elif pitch > 60:  # Half note
            return "hn"
        elif pitch > 48:  # Quarter note
            return "qn"
        elif pitch > 36:  # Eighth note
            return "en"
        else:  # Sixteenth note
            return "sn"

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    gui = SymphonyLangGUI(root)
    root.mainloop()
