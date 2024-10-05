import mido
from mido import MidiFile, MidiTrack, Message
import pygame
import tempfile

# Function to parse SymphonyLang input and convert it to MIDI
def parse_symphonylang(input_text):
    note_to_midi = {
        'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
        'C#4': 61, 'D#4': 63, 'F#4': 66, 'G#4': 68, 'A#4': 70,
        'Bb3': 58, 'Bb4': 70
    }
    
    duration_mapping = {
        'wn': 1,   # Whole note
        'hn': 0.5, # Half note
        'qn': 0.25, # Quarter note
        'en': 0.125, # Eighth note
        'sn': 0.0625 # Sixteenth note
    }

    midi_file = MidiFile()   # Create a new MIDI file
    track = MidiTrack()      # Create a new MIDI track
    midi_file.tracks.append(track)

    for line in input_text.splitlines():
        tokens = line.split()
        if len(tokens) < 2:
            continue
        note = tokens[0]
        duration = tokens[1]

        if note in note_to_midi and duration in duration_mapping:
            midi_note = note_to_midi[note]
            duration_seconds = int(duration_mapping[duration] * 480)

            # Add note on
            track.append(Message('note_on', note=midi_note, velocity=64, time=0))
            # Add note off after duration
            track.append(Message('note_off', note=midi_note, velocity=64, time=duration_seconds))

    return midi_file

def play_midi(midi_file):
    output_filename = 'output.mid'
    midi_file.save(output_filename)
    
    # Initialize pygame mixer to play the MIDI file
    pygame.mixer.init()
    pygame.mixer.music.load(output_filename)
    pygame.mixer.music.play()

    # Wait for the music to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# MIDI file will be saved as 'output.mid' in the current directory.


# Command-line interface
if __name__ == "__main__":
    print("Welcome to SymphonyLang CLI")
    print("Enter your SymphonyLang text (type 'exit' to finish):")

    input_text = ""
    while True:
        line = input("> ")
        if line.lower() == 'exit':
            break
        input_text += line + "\n"

    # Parse the input and generate MIDI
    midi_file = parse_symphonylang(input_text)

    # Play the generated MIDI
    print("Playing the generated music...")
    play_midi(midi_file)

    print("Done!")
