import tkinter as tk
import ttkbootstrap as ttk
import pygame
import os
from mido import MidiFile

class MIDIPlayer:
    def __init__(self, parent_frame, status_callback):
        self.parent_frame = parent_frame
        self.update_status = status_callback
        self.midi_file = None
        self.visualizer = None  
        
        
        pygame.mixer.init()
        
        self.setup_player_controls()

    def setup_player_controls(self):
        
        self.player_label = ttk.Label(self.parent_frame, text="No MIDI file generated yet")
        self.player_label.pack(pady=20)

        self.play_button = ttk.Button(self.parent_frame, text="Play", 
                                    command=self.play_midi, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.stop_button = ttk.Button(self.parent_frame, text="Stop", 
                                    command=self.stop_midi, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def set_visualizer(self, visualizer):
        """Sets the visualizer component."""
        self.visualizer = visualizer

    def play_midi(self):
        """Plays the MIDI file and starts visualization."""
        if self.midi_file and os.path.exists(self.midi_file):
            try:
                pygame.mixer.music.load(self.midi_file)
                pygame.mixer.music.play()
                self.update_status("Playing MIDI file", "info")
                if self.visualizer:
                    self.visualizer.visualize_midi(self.midi_file)
            except pygame.error as e:
                self.update_status(f"Error playing MIDI: {str(e)}", "error")
        else:
            self.update_status("No MIDI file available to play", "warning")

    def stop_midi(self):
        """Stops MIDI playback and visualization."""
        pygame.mixer.music.stop()
        if self.visualizer:
            self.visualizer.stop_visualization()
        self.update_status("Playback stopped", "info")

    def set_midi_file(self, file_path):
        """Sets the MIDI file path."""
        self.midi_file = file_path
        self.player_label.config(text=f"MIDI file generated: {os.path.basename(file_path)}")

    def enable_controls(self, enable=True):
        """Enables or disables player controls."""
        state = tk.NORMAL if enable else tk.DISABLED
        self.play_button.config(state=state)
        self.stop_button.config(state=state)
