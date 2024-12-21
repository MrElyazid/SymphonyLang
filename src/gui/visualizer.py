import tkinter as tk
import colorsys
from mido import MidiFile

class Visualizer:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.visualization_running = False
        self.active_notes = []
        
        
        self.visualization_canvas = tk.Canvas(
            parent_frame,
            width=500,
            height=200,
            bg="#1e1e1e" # Dark background
        )
        self.visualization_canvas.pack(pady=10)

        # Canvas dimensions
        self.canvas_width = 500
        self.canvas_height = 200

    def draw_bar_chart(self):
        """Draws a bar chart with heights based on note pitch and colors based on position in octave."""
        self.visualization_canvas.delete("all")
        if not self.active_notes:
            return

        # Constants for visualization
        bar_width = 30
        min_pitch = 21  # A0 (lowest piano key)
        max_pitch = 108  # C8 (highest piano key)
        pitch_range = max_pitch - min_pitch
        max_height = 180  # Maximum bar height

        # Calculate spacing between bars
        total_width = len(self.active_notes) * bar_width
        spacing = min((self.canvas_width - total_width) / (len(self.active_notes) + 1), 50)
        
        # Draw each active note
        for i, (pitch, velocity) in enumerate(self.active_notes):
            
            x_position = spacing + (i * (bar_width + spacing))

            
            normalized_pitch = (pitch - min_pitch) / pitch_range
            height = normalized_pitch * max_height

            x1 = x_position
            y1 = self.canvas_height - height  # Invert the height for visualization
            x2 = x1 + bar_width
            y2 = self.canvas_height

            # Calculate color based on note position in octave
            note_in_octave = (pitch - min_pitch) % 12
            hue = note_in_octave / 12
            saturation = 0.7
            value = 0.8 + ((velocity / 127) * 0.2)
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'

            # Draw the bar
            self.visualization_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#2d2d2d",  # Slight outline for separation
                width=1
            )

            # Add note name label in white
            note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            note_name = note_names[note_in_octave]
            octave = (pitch - min_pitch) // 12
            
            # self.visualization_canvas.create_text(
            #     (x1 + x2) / 2, y1 - 10,
            #     text=f"{note_name}{octave}",
            #     fill="white",  # White text for dark background
            #     font=("Helvetica", 8)
            # )

    def visualize_midi(self, midi_file):
        """Visualizes the MIDI notes on the bar chart."""
        if not midi_file:
            return
        midi = MidiFile(midi_file)
        self.visualization_running = True
        self.active_notes = []

        # Iterate over MIDI messages and update active notes
        for msg in midi.play():
            if not self.visualization_running:
                break

            if msg.type == "note_on" and msg.velocity > 0:
                # Add note to active notes
                self.active_notes.append((msg.note, msg.velocity))
                self.draw_bar_chart()
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                # Remove note from active notes
                self.active_notes = [(n, v) for n, v in self.active_notes if n != msg.note]
                self.draw_bar_chart()
            
            self.visualization_canvas.update()

    def stop_visualization(self):
        """Stops the visualization."""
        self.visualization_running = False
        self.active_notes = []  # Clear active notes
        self.visualization_canvas.delete("all")  # Clear the canvas
