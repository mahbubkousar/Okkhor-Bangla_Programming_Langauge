import re
from .token_types import TokenType
from .token import Token


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source_code[0] if source_code else None

        # Bengali Unicode ranges: \u0980-\u09FF
        self.KEYWORDS = {
            'মূলকাজ': TokenType.MAIN,
            'ফেরত': TokenType.RETURN,
            'যদি': TokenType.IF,
            'নয়ত': TokenType.ELSE,
            'অথবা': TokenType.ELSE_IF,
            'যতক্ষণ': TokenType.WHILE,
            'কাজ': TokenType.FUNCTION,
            'সংখ্যা': TokenType.INTEGER,
            'দশমিক': TokenType.FLOAT,
            'অক্ষর': TokenType.CHAR,
            'কথা': TokenType.STRING,
            'সত্যমিথ্যা': TokenType.BOOLEAN,
            'সত্য': TokenType.TRUE,
            'মিথ্যা': TokenType.FALSE
        }

        # Regex patterns
        self.PATTERNS = [
            (r'[\u0980-\u09FF]+', self._handle_bengali_word),
            (r'[a-zA-Z_]\w*', self._handle_identifier),
            (r'\d*\.\d+', self._handle_float),
            (r'\d+', self._handle_integer),
            (r'"[^"]*"', self._handle_string),
            (r"'[^']*'", self._handle_char),
            (r'==|!=|<=|>=|[+\-*/%=<>()]', self._handle_operator),
            (r'[ \t]+', None),  # Skip whitespace
            (r'\n', self._handle_newline),
            (r';', lambda m: Token(TokenType.SEMICOLON, m.group(), self.line, self.column)),
            (r',', lambda m: Token(TokenType.COMMA, m.group(), self.line, self.column)),
            (r'{', lambda m: Token(TokenType.LBRACE, m.group(), self.line, self.column)),
            (r'}', lambda m: Token(TokenType.RBRACE, m.group(), self.line, self.column)),
        ]

        # Combined pattern
        self.MASTER_PATTERN = '|'.join(f'({pattern})' for pattern, _ in self.PATTERNS)

    def _handle_bengali_word(self, match):
        value = match.group()
        token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
        return Token(token_type, value, self.line, self.column)

    def _handle_identifier(self, match):
        return Token(TokenType.IDENTIFIER, match.group(), self.line, self.column)

    def _handle_float(self, match):
        return Token(TokenType.NUMBER_LITERAL, float(match.group()), self.line, self.column)

    def _handle_integer(self, match):
        return Token(TokenType.NUMBER_LITERAL, int(match.group()), self.line, self.column)

    def _handle_string(self, match):
        return Token(TokenType.STRING_LITERAL, match.group()[1:-1], self.line, self.column)

    def _handle_char(self, match):
        return Token(TokenType.CHAR_LITERAL, match.group()[1:-1], self.line, self.column)

    def _handle_operator(self, match):
        op_map = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '=': TokenType.ASSIGN,
            '==': TokenType.EQUALS,
            '!=': TokenType.NOT_EQUALS,
            '>': TokenType.GREATER,
            '<': TokenType.LESS,
            '>=': TokenType.GREATER_EQUAL,
            '<=': TokenType.LESS_EQUAL,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
        }
        return Token(op_map[match.group()], match.group(), self.line, self.column)

    def _handle_newline(self, match):
        self.line += 1
        self.column = 1
        return None

    def tokenize(self):
        tokens = []
        position = 0

        while position < len(self.source_code):
            match = re.match(self.MASTER_PATTERN, self.source_code[position:], re.UNICODE)

            if match:
                # Find which pattern matched
                for i, (pattern, handler) in enumerate(self.PATTERNS):
                    group = match.group(i + 1)
                    if group:
                        if handler:  # If there's a handler, process the token
                            token = handler(match)
                            if token:  # Only add non-None tokens (filters out whitespace)
                                tokens.append(token)
                        break

                position += len(match.group(0))
                self.column += len(match.group(0))
            else:
                # Handle invalid character
                char = self.source_code[position]
                tokens.append(Token(TokenType.INVALID, char, self.line, self.column))
                position += 1
                self.column += 1

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens


# src/utils/error_handler.py
class LexerError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")


# main.py
from src.lexer.lexer import Lexer


def main():
    # Example usage
    source_code = '''
    মূলকাজ() {
        সংখ্যা x = ১০;
        যদি (x > ৫) {
            ফেরত x;
        }
    }
    '''

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()