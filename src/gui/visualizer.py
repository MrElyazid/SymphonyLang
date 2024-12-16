import tkinter as tk
import random
from mido import MidiFile

class Visualizer:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.visualization_running = False
        self.note_positions = []  # Store positions of notes for visualization
        
        # Bar chart-like visualization canvas
        self.visualization_canvas = tk.Canvas(parent_frame, width=500, height=200, bg="white")
        self.visualization_canvas.pack(pady=10)

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

            # Draw the bar with a smooth transition effect
            self.visualization_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

            # Add a label with the note duration
            self.visualization_canvas.create_text((x1 + x2) / 2, y1 - 10, text=duration, 
                                               fill="black", font=("Helvetica", 8))

            # Update the x_offset for the next bar
            x_offset = x2 + bar_gap

    def get_random_pastel_color(self):
        """Generates a random pastel color."""
        r = random.randint(200, 255)
        g = random.randint(200, 255)
        b = random.randint(200, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def visualize_midi(self, midi_file):
        """Visualizes the MIDI notes on the bar chart."""
        if not midi_file:
            return
        midi = MidiFile(midi_file)
        self.visualization_running = True

        # Iterate over MIDI messages and track note positions for the graph
        for msg in midi.play():
            if not self.visualization_running:
                break
            if msg.type == "note_on" and msg.velocity > 0:
                # Store the time, pitch, and note duration for visualization
                note_duration = self.get_note_duration(msg.note)
                self.note_positions.append((msg.time * 10, msg.note, note_duration))
                self.draw_bar_chart()
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                self.note_positions.append((msg.time * 10, 200, "sn"))
                self.draw_bar_chart()
            self.visualization_canvas.update()

    def stop_visualization(self):
        """Stops the visualization."""
        self.visualization_running = False
        self.note_positions.clear()  # Clear previous note positions
        self.visualization_canvas.delete("all")  # Clear the canvas

    def get_note_duration(self, pitch):
        """Determines the note duration based on pitch."""
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
