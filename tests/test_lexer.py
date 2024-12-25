# tests/test_lexer.py
import unittest
from src.lexer.lexer import Lexer
from src.lexer.token_types import TokenType


class TestLexer(unittest.TestCase):
    def setUp(self):
        # Helper function to extract token types from a source code
        self.get_token_types = lambda source: [token.type for token in Lexer(source).tokenize()]
        self.get_token_values = lambda source: [token.value for token in Lexer(source).tokenize()]

    def test_keywords(self):
        """Test all Bengali keywords"""
        source = """
        মূলকাজ কাজ সংখ্যা দশমিক অক্ষর কথা সত্যমিথ্যা
        যদি নয়ত অথবা যতক্ষণ
        সত্য মিথ্যা
        """
        tokens = Lexer(source).tokenize()

        # Remove EOF token for checking
        tokens = [t for t in tokens if t.type != TokenType.EOF]

        expected_types = [
            TokenType.MAIN,
            TokenType.FUNCTION,
            TokenType.INTEGER,
            TokenType.FLOAT,
            TokenType.CHAR,
            TokenType.STRING,
            TokenType.BOOLEAN,
            TokenType.IF,
            TokenType.ELSE,
            TokenType.ELSE_IF,
            TokenType.WHILE,
            TokenType.TRUE,
            TokenType.FALSE
        ]

        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)

    def test_numbers(self):
        """Test number literals including Bengali numerals"""
        source = "123 ১২৩ 45.67 ৪৫.৬৭"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Filter out EOF and print debug information
        tokens = [t for t in tokens if t.type != TokenType.EOF]

        # Debug print
        print("\nDebug information for test_numbers:")
        print(f"Source: {source}")
        print("Tokens found:")
        for i, token in enumerate(tokens):
            print(f"{i + 1}. Type: {token.type}, Value: {token.value}, Line: {token.line}, Column: {token.column}")

        # Check if all tokens are number literals
        self.assertTrue(all(token.type == TokenType.NUMBER_LITERAL for token in tokens),
                        "All tokens should be number literals")

        # Check the exact number of tokens
        self.assertEqual(len(tokens), 4,
                         f"Expected 4 number tokens, but got {len(tokens)}")

        # Check individual values
        expected_values = [123, 123, 45.67, 45.67]  # The lexer should convert Bengali numerals
        actual_values = [token.value for token in tokens]

        self.assertEqual(actual_values, expected_values,
                         f"Expected values {expected_values}, but got {actual_values}")

    def test_strings_and_chars(self):
        """Test string and character literals"""
        source = '"Hello বাংলা" \'ক\''
        tokens = Lexer(source).tokenize()
        tokens = [t for t in tokens if t.type != TokenType.EOF]

        self.assertEqual(tokens[0].type, TokenType.STRING_LITERAL)
        self.assertEqual(tokens[0].value, "Hello বাংলা")
        self.assertEqual(tokens[1].type, TokenType.CHAR_LITERAL)
        self.assertEqual(tokens[1].value, "ক")

    def test_operators(self):
        """Test all operators"""
        source = "+ - * / % = == != > < >= <= ( ) { } ; ,"
        tokens = Lexer(source).tokenize()
        tokens = [t for t in tokens if t.type != TokenType.EOF]

        expected_types = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
            TokenType.DIVIDE, TokenType.MODULO, TokenType.ASSIGN,
            TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.GREATER,
            TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL,
            TokenType.LPAREN, TokenType.RPAREN, TokenType.LBRACE,
            TokenType.RBRACE, TokenType.SEMICOLON, TokenType.COMMA
        ]

        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)

    def test_identifiers(self):
        """Test Bengali and English identifiers"""
        source = "variable বাংলা_নাম mixed_বাংলা"
        tokens = Lexer(source).tokenize()
        tokens = [t for t in tokens if t.type != TokenType.EOF]

        for token in tokens:
            self.assertEqual(token.type, TokenType.IDENTIFIER)

    def test_complete_program(self):
        """Test a complete program structure"""
        source = """
        মূলকাজ() {
            সংখ্যা নাম্বার = ১২৩;
            কথা বার্তা = "হ্যালো";
            যদি (নাম্বার > ১০০) {
                ফেরত সত্য;
            }
            নয়ত {
                ফেরত মিথ্যা;
            }
        }
        """
        tokens = Lexer(source).tokenize()

        # Print debug information
        print("\nDebug information for test_complete_program:")
        print("Tokens found:")
        for i, token in enumerate(tokens):
            if token.type != TokenType.EOF:
                print(f"{i + 1}. Type: {token.type}, Value: {token.value}, Line: {token.line}, Column: {token.column}")

        # Verify no invalid tokens
        invalid_tokens = [t for t in tokens if t.type == TokenType.INVALID]
        self.assertEqual(len(invalid_tokens), 0,
                         f"Found invalid tokens: {invalid_tokens}")

        # Verify line numbers are tracked
        self.assertTrue(all(hasattr(t, 'line') for t in tokens))
        self.assertTrue(all(hasattr(t, 'column') for t in tokens))

    def test_invalid_characters(self):
        """Test handling of invalid characters"""
        source = "সংখ্যা x = @#$;"
        tokens = Lexer(source).tokenize()

        # Print debug information
        print("\nDebug information for test_invalid_characters:")
        print("Tokens found:")
        for i, token in enumerate(tokens):
            if token.type != TokenType.EOF:
                print(f"{i + 1}. Type: {token.type}, Value: {token.value}, Line: {token.line}, Column: {token.column}")

        invalid_tokens = [t for t in tokens if t.type == TokenType.INVALID]
        self.assertTrue(len(invalid_tokens) > 0,
                        "Should have found invalid tokens")


if __name__ == '__main__':
    unittest.main(verbosity=2)