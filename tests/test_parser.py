import pytest
from src.parser import parse_symphony_lang, SymphonyLangParserError, MusicElement

def test_parse_basic_note():
    input_text = """
    tempo=120
    C4 qn
    """
    result = parse_symphony_lang(input_text)
    assert result.tempo == 120
    assert len(result.elements) == 1
    assert isinstance(result.elements[0], MusicElement)
    assert result.elements[0].type == 'note'
    assert result.elements[0].value == 'C4'
    assert result.elements[0].duration == 'qn'

def test_parse_scale():
    input_text = """
    tempo=120
    C4 maj pent
    """
    result = parse_symphony_lang(input_text)
    assert result.tempo == 120
    assert len(result.elements) == 1
    assert result.elements[0].type == 'scale'
    assert result.elements[0].value['root'] == 'C4'
    assert result.elements[0].value['type'] == 'maj'
    assert result.elements[0].value['extension'] == 'pent'

def test_parse_chord():
    input_text = """
    tempo=120
    [C4 E4 G4] wn
    """
    result = parse_symphony_lang(input_text)
    assert result.tempo == 120
    assert len(result.elements) == 1
    assert result.elements[0].type == 'chord'
    assert result.elements[0].value == ['C4', 'E4', 'G4']
    assert result.elements[0].duration == 'wn'

def test_parse_rest():
    input_text = """
    tempo=120
    qr
    """
    result = parse_symphony_lang(input_text)
    assert result.tempo == 120
    assert len(result.elements) == 1
    assert result.elements[0].type == 'rest'
    assert result.elements[0].duration == 'qr'

def test_parse_multiple_elements():
    input_text = """
    tempo=120
    C4 qn
    D4 hn
    qr
    [E4 G4] wn
    """
    result = parse_symphony_lang(input_text)
    assert result.tempo == 120
    assert len(result.elements) == 4
    # First element - note
    assert result.elements[0].type == 'note'
    assert result.elements[0].value == 'C4'
    # Second element - note
    assert result.elements[1].type == 'note'
    assert result.elements[1].value == 'D4'
    # Third element - rest
    assert result.elements[2].type == 'rest'
    # Fourth element - chord
    assert result.elements[3].type == 'chord'
    assert result.elements[3].value == ['E4', 'G4']

def test_missing_tempo():
    input_text = """
    C4 qn
    """
    with pytest.raises(SymphonyLangParserError):
        parse_symphony_lang(input_text)

def test_invalid_syntax():
    input_text = """
    tempo=120
    C4 qn D4
    """
    with pytest.raises(SymphonyLangParserError):
        parse_symphony_lang(input_text)
