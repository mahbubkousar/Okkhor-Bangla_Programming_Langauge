from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    MAIN = auto()  # মূলকাজ
    RETURN = auto()  # ফেরত
    IF = auto()  # যদি
    ELSE = auto()  # নয়ত
    ELSE_IF = auto()  # অথবা
    WHILE = auto()  # যতক্ষণ
    FUNCTION = auto()  # কাজ

    # Data Types
    INTEGER = auto()  # সংখ্যা
    FLOAT = auto()  # দশমিক
    CHAR = auto()  # অক্ষর
    STRING = auto()  # কথা
    BOOLEAN = auto()  # সত্যমিথ্যা

    # Literals
    NUMBER_LITERAL = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()
    TRUE = auto()  # সত্য
    FALSE = auto()  # মিথ্যা

    # Operators
    PLUS = auto()  # +
    MINUS = auto()  # -
    MULTIPLY = auto()  # *
    DIVIDE = auto()  # /
    MODULO = auto()  # %
    ASSIGN = auto()  # =

    # Comparisons
    EQUALS = auto()  # ==
    NOT_EQUALS = auto()  # !=
    GREATER = auto()  # >
    LESS = auto()  # <
    GREATER_EQUAL = auto()  # >=
    LESS_EQUAL = auto()  # <=

    # Delimiters
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,

    # Other
    IDENTIFIER = auto()  # Variable and function names
    EOF = auto()  # End of file
    INVALID = auto()  # Invalid token