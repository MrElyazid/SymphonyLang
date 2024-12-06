import ply.lex as lex

class SymphonyLangLexerError(Exception):
    pass

#Tokens
tokens = (
    'NOTE',
    'DURATION',
    'TEMPO',
    'NUMBER',
    'NEWLINE',
    'EQUALS',
)

#Regular Expressions for tokens
t_NOTE = r'[A-G](\#|b)?[0-9]'
t_DURATION = r'wn|hn|qn|en|sn'
t_TEMPO = r'tempo'
t_EQUALS = r'='


#number token rule
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


#newline token rule
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

#comment token rule
def t_COMMENT(t):
    r'\#.*'
    pass  # 7it baghin a nfoto comments o safi donc mandiro walo

#dima kn7tajo hadi :
t_ignore = ' \t'

#raise an error if we encounter a token we didnt define
def t_error(t):
    raise SymphonyLangLexerError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# and finally build the lexer, rah automatically gonna use the tokens definitions and rules
lexer = lex.lex()

def get_all_tokens(input_string):
    lexer.input(input_string)
    
    # normalement mni anjiw nkhdmo b lexer mn parser.py n9dro gha n importiwh o safi, had while loop gha la bghina nakhdo tokens f list
    token_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_list.append(tok)
    return token_list

# had part kin f aghlabiya dyal les fichiers (mbdl l kola file), purpose howa testing dyal code li fl file mni n runniwh bohdo
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
