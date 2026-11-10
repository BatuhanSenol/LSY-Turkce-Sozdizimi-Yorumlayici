from re import finditer
from unicodedata import normalize
from error import SYNTAXERROR

TOKEN_SPEC = [
    ('NUMBER',    r'\d+'),
    ('PLUS',      r'\+'),
    ('MINUS',     r'-'),
    ('STAR',      r'\*'),
    ('COMMENT',   r'//[^\n]*'),
    ('SLASH',     r'/'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('SKIP',      r'[ \t\n]+'),
    ('SEMICOLON', r';'),
    ('COLON',     r':'),
    ('EQEQ',      r'=='),
    ('EQ',        r'='),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('LT',        r'<'),
    ('GT',        r'>'),
    ('NEQ',       r'!='),
    ('STRING',    r'"(?:\\.|[^"\\])*"'),
    ('COMMA',     r','),
    ('DOT',       r'\.'),
    ('IDENT',     r'[^\W\d]\w*'),
    ('UNKNOWN',   r'.'),
]

KEYWORDS = {
    'if':     ("eger", "eğer"),
    'while':  ("iken",),
    'else':   ("degilse", "değilse","yoksa",),
    'fn':     ("fon","fn",),
    'call':   ("cagir", "çağır"),
    'print':  ("yaz",),
    'repeat': ("tekrar",),
    'sleep':  ("uyu","bekle",),
    'use':    ("kullan",),
    'del':    ("sil",),
    'scope':  ("kapsam",),
}

def tr_lower(s: str) -> str:
    return s.replace('İ', 'i').replace('I', 'ı').lower()






KEYWORD_MAP = {
    tr_word: en_name.upper()
    for en_name, tr_words in KEYWORDS.items()
    for tr_word in tr_words
}


# ... KEYWORDS / KEYWORD_MAP / tr_lower yukarıdaki gibi ...

def lexer_engine(code: str = "", file_name: str = ""):
    code = normalize("NFC", code)
    tokens = []
    master_pattern = '|'.join(f'(?P<{n}>{p})' for n, p in TOKEN_SPEC)
    line = 1

    for match in finditer(master_pattern, code):
        kind, value, token_line = match.lastgroup, match.group(), line

        if kind == 'COMMENT':
            kind = 'SKIP'
        if kind == 'SKIP':
            line += value.count('\n')
            continue
        if kind == 'UNKNOWN':
            SYNTAXERROR.error(token_line, ErrorFile=file_name, ErrorElement=value)
        if kind == 'IDENT':
            kind = KEYWORD_MAP.get(tr_lower(value), kind)
        tokens.append((kind, value, token_line))

    tokens.append(("EOF", None, line))
    return tokens