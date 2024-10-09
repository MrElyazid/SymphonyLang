import mido
from parser import Composition, MusicElement

class MIDIGenerationError(Exception):
    pass

NOTE_TO_MIDI = {
    'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71
}

DURATION_TO_TICKS = {
    'wn': 1920, 'hn': 960, 'qn': 480, 'en': 240, 'sn': 120
}

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

def generate_midi(composition: Composition, output_file: str):
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(composition.tempo)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    for element in composition.elements:
        if isinstance(element, MusicElement) and element.type == 'note':
            try:
                midi_note = note_to_midi_number(element.value)
                duration = DURATION_TO_TICKS[element.duration]
            except KeyError:
                raise MIDIGenerationError(f"Invalid duration: {element.duration}")

            velocity = 64  # Default velocity, can be adjusted for dynamics later
            track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=0))
            track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=duration))

    try:
        mid.save(output_file)
    except IOError:
        raise MIDIGenerationError(f"Unable to save MIDI file: {output_file}")

if __name__ == "__main__":
    test_composition = Composition(
        tempo=120,
        elements=[
            MusicElement('note', 'C4', 'qn'),
            MusicElement('note', 'D4', 'hn'),
            MusicElement('note', 'E4', 'qn'),
            MusicElement('note', 'F4', 'wn'),
        ]
    )
    try:
        generate_midi(test_composition, 'test_output.mid')
        print("MIDI file generated: test_output.mid")
    except MIDIGenerationError as e:
        print(f"Error generating MIDI file: {str(e)}")