import re

# Token types
TOKENS = [
    ('KEYWORD', r'\b(vibe|spill|funk|delulu|nah)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('STRING', r'"[^"]*"'),
    ('SYMBOL', r'[{}();,=><+\-*/]'),
    ('WHITESPACE', r'\s+'),
]

TOKEN_REGEX = re.compile('|'.join(f'(?P<{name}>{regex})' for name, regex in TOKENS))

def tokenize(code):
    tokens = []
    for match in TOKEN_REGEX.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind != 'WHITESPACE':
            tokens.append((kind, value))
    return tokens
