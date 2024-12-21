import ply.lex as lex

class SymphonyLangLexerError(Exception):
    pass

tokens = (
    'NOTE',
    'DURATION',
    'TEMPO',
    'NUMBER',
    'NEWLINE',
    'EQUALS',
    'SCALE_TYPE',
    'SCALE_EXTENSION',
    'CHORD',
    'REST',
    'LBRACKET',
    'RBRACKET'
)

t_NOTE = r'[A-G](\#|b)?[0-9]'
t_DURATION = r'wn|hn|qn|en|sn'
t_TEMPO = r'tempo'
t_EQUALS = r'='
t_REST = r'wr|hr|qr|er|sr'
t_SCALE_TYPE = r'maj|min'
t_SCALE_EXTENSION = r'pent|chrom'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'



def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

t_ignore = ' \t'

def t_error(t):
    raise SymphonyLangLexerError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

lexer = lex.lex()

def get_all_tokens(input_string):
    lexer.input(input_string)
    
    token_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_list.append(tok)
    return token_list

if __name__ == "__main__":
    test_input = """
    # This is a test input
    tempo=120
    C4 qn
    qr
    C4 maj
    [C4 E4] wn
    """
    try:
        tokens = get_all_tokens(test_input)
        for token in tokens:
            print(token)
    except SymphonyLangLexerError as e:
        print(f"Lexer Error: {str(e)}")