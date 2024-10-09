import ply.yacc as yacc
from lexer import tokens, SymphonyLangLexerError

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

# Grammar rules
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

# Ensure element correctly captures NEWLINE
def p_element(p):
    '''element : note
               | NEWLINE'''  # Modify to allow NEWLINE as its own element
    if len(p) == 2 and isinstance(p[1], MusicElement):
        p[0] = p[1]
    else:
        p[0] = None
        

def p_note(p):
    'note : NOTE DURATION'
    p[0] = MusicElement('note', p[1], p[2])

def p_error(p):
    if p:
        raise SymphonyLangParserError(f"Syntax error at token {p.type} with value '{p.value}' at line {p.lineno}")
    else:
        raise SymphonyLangParserError("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Function to parse SymphonyLang
def parse_symphony_lang(input_text):
    try:
        return parser.parse(input_text)
    except SymphonyLangLexerError as e:
        raise SymphonyLangParserError(f"Lexer error: {str(e)}")

# Test the parser
if __name__ == "__main__":
    test_input = """
    # This is a test input
    tempo=120
    C4 qn  # This is middle C
    D4 hn
    E4 qn
    F4 wn
    """
    try:
        result = parse_symphony_lang(test_input)
        print(f"Parsed composition: {result}")
        print(f"Tempo: {result.tempo}")
        for element in result.elements:
            if isinstance(element, MusicElement):
                print(f"Note: {element.value}, Duration: {element.duration}")
    except SymphonyLangParserError as e:
        print(f"Parser Error: {str(e)}")
