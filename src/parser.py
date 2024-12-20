import ply.yacc as yacc
from lexer import SymphonyLangLexerError, tokens, lexer

class SymphonyLangParserError(Exception):
    pass

class MusicElement:
    def __init__(self, element_type, value=None, duration=None):
        self.type = element_type
        self.value = value
        self.duration = duration

    def __repr__(self):
        return f"MusicElement({self.type}, {self.value}, {self.duration})"

class Composition:
    def __init__(self, tempo, elements):
        self.tempo = tempo
        self.elements = elements

    def __repr__(self):
        return f"Composition(tempo={self.tempo}, elements={self.elements})"

def p_composition(p):
    '''composition : tempo_setting element_list'''
    p[0] = Composition(p[1], p[2])

def p_tempo_setting(p):
    'tempo_setting : TEMPO EQUALS NUMBER'
    p[0] = p[3]

def p_element_list(p):
    '''element_list : element
                    | element_list element'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_element(p):
    '''element : note
               | scale
               | chord
               | rest
               | NEWLINE'''
    if len(p) == 2 and isinstance(p[1], MusicElement):
        p[0] = p[1]
    else:
        p[0] = None

def p_rest(p):
    '''rest : REST'''
    p[0] = MusicElement('rest', None, p[1])

def p_note(p):
    '''note : NOTE DURATION'''
    p[0] = MusicElement('note', p[1], p[2])

def p_scale(p):
    '''scale : NOTE SCALE_TYPE
             | NOTE SCALE_TYPE SCALE_EXTENSION'''
    if len(p) == 3:
        scale_value = {
            'root': p[1],
            'type': p[2],
            'extension': None
        }
    elif len(p) == 4:
        scale_value = {
            'root': p[1],
            'type': p[2],
            'extension': p[3]
        }
    p[0] = MusicElement('scale', scale_value, 'qn')

def p_chord(p):
    '''chord : LBRACKET note_list RBRACKET DURATION'''
    p[0] = MusicElement('chord', p[2], p[4])

def p_note_list(p):
    '''note_list : NOTE
                 | note_list NOTE'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_error(p):
    if p:
        raise SymphonyLangParserError(f"Syntax error at token {p.type} with value '{p.value}' at line {p.lineno}")
    else:
        raise SymphonyLangParserError("Syntax error at EOF")

parser = yacc.yacc()

def parse_symphony_lang(input_text):
    try:
        lexer.input(input_text.strip())
        return parser.parse(lexer=lexer)
    except SymphonyLangLexerError as e:
        raise SymphonyLangParserError(f"Lexer error: {str(e)}")

if __name__ == "__main__":
    test_input = """
    tempo=120
    C4 qn  # This is middle C
    D4 hn
    E4 qn
    F4 wn
    C4 maj  # Test major scale
    A4 min pent  # Test pentatonic minor scale
    [C4 E4 G4] wn  # Test chord
    """
    try:
        result = parse_symphony_lang(test_input)
        print(f"Parsed composition: {result}")
        print(f"Tempo: {result.tempo}")
        for element in result.elements:
            if isinstance(element, MusicElement):
                print(f"Type: {element.type}, Value: {element.value}, Duration: {element.duration}")
    except SymphonyLangParserError as e:
        print(f"Parser Error: {str(e)}")
