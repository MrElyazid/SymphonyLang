import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.player import MIDIPlayer
from gui.visualizer import Visualizer
from gui.file_handler import FileHandler

class SymphonyLangGUI:
    def __init__(self, master):
        self.master = master
        master.title("SymphonyLang")
        master.geometry("900x600")

        # Initialize frames first
        self.setup_main_frame()
        self.setup_frames()
        
        # Initialize text input and status message
        self.setup_text_input()
        self.setup_status_message()
        
        # Initialize sub-components
        self.player = MIDIPlayer(self.right_frame, self.update_status)
        self.visualizer = Visualizer(self.right_frame)
        
        # Connect player and visualizer
        self.player.set_visualizer(self.visualizer)
        
        # Initialize file handler
        self.file_handler = FileHandler(self.input_text, self.update_status, 
                                      self.player.set_midi_file,
                                      self.player.enable_controls)
        
        # Setup buttons last since they depend on file_handler
        self.setup_buttons()

    def setup_main_frame(self):
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    def setup_frames(self):
        # Left frame for input
        self.left_frame = ttk.Frame(self.main_frame, width=400)
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # Right frame for player and visualization
        self.right_frame = ttk.Frame(self.main_frame, width=500)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

    def setup_text_input(self):
        # Text input
        self.input_text = tk.Text(self.left_frame, wrap=tk.WORD, width=40, height=20)
        self.input_text.pack(fill=BOTH, expand=YES, pady=(0, 10))

    def setup_buttons(self):
        # Buttons
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(fill=X)

        compile_button = ttk.Button(button_frame, text="Compile", 
                                  command=self.file_handler.compile_code)
        compile_button.pack(side=LEFT, padx=(0, 5))

        upload_button = ttk.Button(button_frame, text="Upload txt", 
                                 command=self.file_handler.upload_txt)
        upload_button.pack(side=LEFT)

    def setup_status_message(self):
        # Status message
        self.status_message = ttk.Label(self.left_frame, text="", wraplength=380)
        self.status_message.pack(fill=X, pady=(10, 0))

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
