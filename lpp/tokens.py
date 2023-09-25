from enum import (
    auto,
    Enum,
    unique
)
from typing import (
    NamedTuple,
    Dict
)
@unique
class TokenType(Enum):
    ASSIGN = auto()
    COMMA = auto()
    FOR = auto()
    EOF = auto()
    WHILE = auto()
    FUNCTION = auto()
    IDENT = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRACE = auto()
    LET = auto()
    LPAREN = auto()
    MINUS = auto()
    PLUS = auto()
    RBRACE = auto()
    RPAREN=auto()
    SEMICOLON = auto()
    EQ = auto()
    CLASS = auto()
    

class Token(NamedTuple):
    token_type:TokenType
    literal:str
    def __str__(self) -> str:
        return f'Type {self.token_type}, Literal {self.literal}'
    

def lookup_token_type(literal:str) -> TokenType:
    keywords: Dict[str,TokenType]={
        'variable':TokenType.LET,
        'function':TokenType.FUNCTION,
        #SE AGREGA LA PALABRA y el identificador dle token
        'for':TokenType.FOR,
        'mientras':TokenType.WHILE,
        'clase':TokenType.CLASS

    }
    return keywords.get(literal,TokenType.IDENT)