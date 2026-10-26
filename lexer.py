from re import finditer

from error import SYNTAXERROR

TOKEN_SPEC = [
    ('NUMBER',  r'\d+'),
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
    ('STAR',    r'\*'),
    ('COMMENT',   r'//[^\n]*'),
    ('SLASH',   r'/'),
    ('LPAREN',  r'\('),
    ('RPAREN',  r'\)'),
    ('SKIP',    r'[ \t\n]+'),
    ('SEMICOLON', r';'),
    ('COLON', r':'),
    ("EQEQ", r"=="),
    ("EQ", r"="),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LT',    r'<'),
    ('GT',    r'>'),
    ('NEQ',   r'!='),
    ("STRING", r'"(?:\\.|[^"\\])*"'),
    ("COMMA", r","),
    ('DOT', r'\.'),
    
    ('IDENT', r'[a-zA-Z_][\w-]*'),
    ("UNKNOWN", r".")
]

KEYWORDS =         {'if', 'while', 'else', 'fn', "call", "print", "repeat", "sleep", "use", "del", "scope"}
TURKISH_KEYWORDS = {}

def lexer_engine(code:str="", file_name:str=""):
    tokens = []
    master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
    line = 1

    for match in finditer(master_pattern, code):
        kind = match.lastgroup
        value = match.group()
        token_line = line

        if kind == 'COMMENT':
            kind = "SKIP"
        if kind == 'SKIP':
            line += value.count('\n')
            continue
        if kind == "UNKNOWN":
            SYNTAXERROR.error(token_line, ErrorFile=file_name, ErrorElement=value)
        if kind == 'IDENT' and value in KEYWORDS:
            kind = value.upper()
        tokens.append((kind, value, token_line))

    tokens.append(("EOF", None, line))
    return tokens