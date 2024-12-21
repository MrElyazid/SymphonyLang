import pytest
from src.lexer import get_all_tokens, SymphonyLangLexerError

def test_basic_note_tokenization():
    input_text = "C4 qn"
    tokens = get_all_tokens(input_text)
    assert len(tokens) == 2
    assert tokens[0].type == 'NOTE'
    assert tokens[0].value == 'C4'
    assert tokens[1].type == 'DURATION'
    assert tokens[1].value == 'qn'

def test_tempo_tokenization():
    input_text = "tempo=120"
    tokens = get_all_tokens(input_text)
    assert len(tokens) == 3
    assert tokens[0].type == 'TEMPO'
    assert tokens[1].type == 'EQUALS'
    assert tokens[2].type == 'NUMBER'
    assert tokens[2].value == 120

def test_scale_tokenization():
    input_text = "C4 maj pent"
    tokens = get_all_tokens(input_text)
    assert len(tokens) == 3
    assert tokens[0].type == 'NOTE'
    assert tokens[1].type == 'SCALE_TYPE'
    assert tokens[2].type == 'SCALE_EXTENSION'

def test_chord_tokenization():
    input_text = "[C4 E4 G4] wn"
    tokens = get_all_tokens(input_text)
    assert len(tokens) == 6
    assert tokens[0].type == 'LBRACKET'
    assert tokens[1].type == 'NOTE'
    assert tokens[2].type == 'NOTE'
    assert tokens[3].type == 'NOTE'
    assert tokens[4].type == 'RBRACKET'
    assert tokens[5].type == 'DURATION'

def test_rest_tokenization():
    input_text = "qr"
    tokens = get_all_tokens(input_text)
    assert len(tokens) == 1
    assert tokens[0].type == 'REST'
    assert tokens[0].value == 'qr'

def test_invalid_character():
    input_text = "C4 qn $"
    with pytest.raises(SymphonyLangLexerError):
        get_all_tokens(input_text)

def test_comment_handling():
    input_text = "C4 qn  # This is a comment"
    tokens = get_all_tokens(input_text)
    assert len(tokens) == 2  # Comments should be ignored
    assert tokens[0].type == 'NOTE'
    assert tokens[1].type == 'DURATION'
