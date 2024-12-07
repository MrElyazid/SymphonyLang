# had l file kayakhod l output dyal parser.py o kay generer audio file ( midi file ), daba parser.py kay produit list ( ngolo arbre )
# dyal objects sminahom MusicElement, role dyal midi_generator ndiro track o n appendiw lih musicelements, walakin en respectant syntax
# dyal mido library, donc khass ndiro translation l kola MusicElement l mido syntax o ndiroh f track


import mido
from parser import Composition, MusicElement

class MIDIGenerationError(Exception):
    pass


# khass ndiro translation l kola MusicElement l syntax li ngdo n generiwh bih b mido library matalan note dyal C4 haka : 
# track.append(Message('note_on', note=60, velocity=64, time=0)) hnaya C t mappat l 60 dakchi lach khass had dictionnaire

NOTE_TO_MIDI = {
    'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71
}

# nefs lhaja bnisba l duration dyal notes, khass nraj3ohom ticks, google ticks f mido and how to convert them to seconds, atkoun wahed 
# l formule li fiha temp imkn

DURATION_TO_TICKS = {
    'wn': 1920, 'hn': 960, 'qn': 480, 'en': 240, 'sn': 120
}

# Scale patterns defined in semitones (half steps)
SCALE_PATTERNS = {
    'maj': [0, 2, 4, 5, 7, 9, 11, 12],  # Major scale
    'min': [0, 2, 3, 5, 7, 8, 10, 12],  # Natural minor scale
    'maj pent': [0, 2, 4, 7, 9, 12],    # Major pentatonic
    'min pent': [0, 3, 5, 7, 10, 12],   # Minor pentatonic
    'chrom': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Chromatic scale
}

# fonction li kadir l conversion

def note_to_midi_number(note):
    try:
        base_note = note[0]
        octave = int(note[-1])
        midi_number = NOTE_TO_MIDI[base_note] + (octave - 4) * 12
        if '#' in note:
            midi_number += 1
        elif 'b' in note:
            midi_number -= 1
        return midi_number
    except (KeyError, ValueError, IndexError):
        raise MIDIGenerationError(f"Invalid note: {note}")

def generate_scale_notes(root_note, scale_type, extension=None):
    """Generate MIDI note numbers for a scale starting from root_note"""
    try:
        root_midi = note_to_midi_number(root_note)
        scale_key = f"{scale_type} {extension}" if extension else scale_type
        
        if scale_key not in SCALE_PATTERNS:
            raise MIDIGenerationError(f"Unsupported scale type: {scale_key}")
        
        pattern = SCALE_PATTERNS[scale_key]
        return [root_midi + interval for interval in pattern]
    except Exception as e:
        raise MIDIGenerationError(f"Error generating scale: {str(e)}")

def generate_midi(composition: Composition, output_file: str):
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(composition.tempo)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    for element in composition.elements:
        if not isinstance(element, MusicElement):
            continue

        if element.type == 'note':
            try:
                midi_note = note_to_midi_number(element.value)
                duration = DURATION_TO_TICKS[element.duration]
            except KeyError:
                raise MIDIGenerationError(f"Invalid duration: {element.duration}")

            velocity = 64  # Default velocity
            track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=0))
            track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=duration))

        elif element.type == 'scale':
            try:
                scale_value = element.value  # Dictionary containing root, type, and extension
                scale_notes = generate_scale_notes(
                    scale_value['root'],
                    scale_value['type'],
                    scale_value['extension']
                )
                
                # Play each note in the scale
                note_duration = DURATION_TO_TICKS['qn']  # Use quarter notes for scales
                velocity = 64
                
                # Play ascending
                for i, midi_note in enumerate(scale_notes):
                    # First note has time=0, others follow previous note
                    time = 0 if i == 0 else note_duration
                    track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=time))
                    track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=note_duration))
                
                # Play descending (excluding the last note as it's the same as first note of next octave)
                for midi_note in reversed(scale_notes[:-1]):
                    track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=note_duration))
                    track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=note_duration))
                
            except Exception as e:
                raise MIDIGenerationError(f"Error processing scale: {str(e)}")

    try:
        mid.save(output_file)
    except IOError:
        raise MIDIGenerationError(f"Unable to save MIDI file: {output_file}")

if __name__ == "__main__":
    test_composition = Composition(
        tempo=120,
        elements=[
            MusicElement('note', 'C4', 'qn'),
            MusicElement('scale', {'root': 'C4', 'type': 'maj', 'extension': None}),
            MusicElement('scale', {'root': 'A4', 'type': 'min', 'extension': 'pent'}),
        ]
    )
    try:
        generate_midi(test_composition, 'test_output.mid')
        print("MIDI file generated: test_output.mid")
    except MIDIGenerationError as e:
        print(f"Error generating MIDI file: {str(e)}")