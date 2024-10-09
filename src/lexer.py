import ply.lex as lex

class SymphonyLangLexerError(Exception):
    pass

# Token types
tokens = (
    'NOTE',
    'DURATION',
    'TEMPO',
    'NUMBER',
    'NEWLINE',
    'EQUALS',  # Added EQUALS to handle '=' sign
)

# Regular expressions for tokens
t_NOTE = r'[A-G](\#|b)?[0-9]'
t_DURATION = r'wn|hn|qn|en|sn'
t_TEMPO = r'tempo'  # The TEMPO token should match 'tempo' without the '='
t_EQUALS = r'='  # Added rule for equals sign

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# Define a rule for comments
def t_COMMENT(t):
    r'\#.*'
    pass  # No return value. Token discarded

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    raise SymphonyLangLexerError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Build the lexer
lexer = lex.lex()

def get_all_tokens(input_string):
    lexer.input(input_string)
    return list(lexer)

# Test the lexer
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
        tokens = get_all_tokens(test_input)
        for token in tokens:
            print(token)
    except SymphonyLangLexerError as e:
        print(f"Lexer Error: {str(e)}")
