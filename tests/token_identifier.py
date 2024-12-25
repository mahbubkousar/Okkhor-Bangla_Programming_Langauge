# token_identifier.py
from src.lexer.lexer import Lexer
from src.lexer.token_types import TokenType


def display_tokens(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    # Group tokens by category
    categories = {
        'Keywords': [],
        'Operators': [],
        'Delimiters': [],
        'Identifiers': [],
        'Literals': [],
        'Invalid': []
    }

    operator_types = {TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE,
                      TokenType.MODULO, TokenType.ASSIGN, TokenType.EQUALS, TokenType.NOT_EQUALS,
                      TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL}

    delimiter_types = {TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE, TokenType.RBRACE,
                       TokenType.SEMICOLON, TokenType.COMMA}

    keyword_types = {TokenType.MAIN, TokenType.FUNCTION, TokenType.INTEGER, TokenType.FLOAT,
                     TokenType.CHAR, TokenType.STRING, TokenType.BOOLEAN, TokenType.IF,
                     TokenType.ELSE, TokenType.ELSE_IF, TokenType.WHILE, TokenType.RETURN,
                     TokenType.TRUE, TokenType.FALSE}

    literal_types = {TokenType.NUMBER_LITERAL, TokenType.STRING_LITERAL, TokenType.CHAR_LITERAL}

    for token in tokens:
        if token.type == TokenType.EOF:
            continue

        if token.type in keyword_types:
            categories['Keywords'].append(token)
        elif token.type in operator_types:
            categories['Operators'].append(token)
        elif token.type in delimiter_types:
            categories['Delimiters'].append(token)
        elif token.type == TokenType.IDENTIFIER:
            categories['Identifiers'].append(token)
        elif token.type in literal_types:
            categories['Literals'].append(token)
        elif token.type == TokenType.INVALID:
            categories['Invalid'].append(token)

    # Display tokens by category
    print("Identified Tokens:\n")
    for category, tokens in categories.items():
        if tokens:
            print(f"{category}:")
            for token in tokens:
                print(f"  {token.value} (Line {token.line}, Column {token.column})")
            print()


# Test with a sample program
sample_program = """
মূলকাজ() {
    সংখ্যা নাম্বার = ১২৩;
    কথা বার্তা = "হ্যালো বাংলা";
    যদি (নাম্বার > ১০০) {
        ফেরত সত্য;
    }
    নয়ত {
        ফেরত মিথ্যা;
    }
}
"""

if __name__ == "__main__":
    print("Analyzing sample program:")
    print("-" * 50)
    print(sample_program)
    print("-" * 50)
    print()
    display_tokens(sample_program)