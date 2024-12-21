import pytest
import os
from src.midi_generator import (
    note_to_midi_number,
    generate_scale_notes,
    generate_midi,
    MIDIGenerationError
)
from src.parser import Composition, MusicElement

def test_note_to_midi_number():
    # Test basic notes
    assert note_to_midi_number('C4') == 60  # Middle C
    assert note_to_midi_number('A4') == 69
    assert note_to_midi_number('G4') == 67

    # Test sharps and flats
    assert note_to_midi_number('C#4') == 61
    assert note_to_midi_number('Bb3') == 58

    # Test different octaves
    assert note_to_midi_number('C5') == 72
    assert note_to_midi_number('C3') == 48

def test_invalid_note_to_midi():
    with pytest.raises(MIDIGenerationError):
        note_to_midi_number('H4')  # Invalid note name
    with pytest.raises(MIDIGenerationError):
        note_to_midi_number('Cx4')  # Invalid accidental

def test_generate_scale_notes():
    # Test major scale
    c_major = generate_scale_notes('C4', 'maj')
    expected_major = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
    assert c_major == expected_major

    # Test minor scale
    a_minor = generate_scale_notes('A4', 'min')
    expected_minor = [69, 71, 72, 74, 76, 77, 79, 81]  # A4 to A5
    assert a_minor == expected_minor

    # Test pentatonic scale
    c_pent = generate_scale_notes('C4', 'maj', 'pent')
    expected_pent = [60, 62, 64, 67, 69, 72]  # C major pentatonic
    assert c_pent == expected_pent

def test_invalid_scale_generation():
    with pytest.raises(MIDIGenerationError):
        generate_scale_notes('C4', 'invalid')  # Invalid scale type
    with pytest.raises(MIDIGenerationError):
        generate_scale_notes('H4', 'maj')  # Invalid note

def test_midi_file_generation():
    # Create a simple composition
    composition = Composition(
        tempo=120,
        elements=[
            MusicElement('note', 'C4', 'qn'),
            MusicElement('note', 'E4', 'qn'),
            MusicElement('note', 'G4', 'qn'),
        ]
    )
    
    test_output = 'test_output.mid'
    
    # Generate MIDI file
    generate_midi(composition, test_output)
    
    # Check if file was created
    assert os.path.exists(test_output)
    
    # Clean up
    os.remove(test_output)

def test_midi_generation_with_all_elements():
    composition = Composition(
        tempo=120,
        elements=[
            MusicElement('note', 'C4', 'qn'),
            MusicElement('rest', None, 'qr'),
            MusicElement('scale', {'root': 'C4', 'type': 'maj', 'extension': None}, 'qn'),
            MusicElement('chord', ['C4', 'E4', 'G4'], 'wn'),
        ]
    )
    
    test_output = 'test_complex.mid'
    
    # Generate MIDI file
    generate_midi(composition, test_output)
    
    # Check if file was created
    assert os.path.exists(test_output)
    
    # Clean up
    os.remove(test_output)

def test_invalid_midi_generation():
    # Test with invalid note
    invalid_composition = Composition(
        tempo=120,
        elements=[MusicElement('note', 'H4', 'qn')]
    )
    
    with pytest.raises(MIDIGenerationError):
        generate_midi(invalid_composition, 'test_invalid.mid')

    # Test with invalid duration
    invalid_composition = Composition(
        tempo=120,
        elements=[MusicElement('note', 'C4', 'invalid')]
    )
    
    with pytest.raises(MIDIGenerationError):
        generate_midi(invalid_composition, 'test_invalid.mid')
