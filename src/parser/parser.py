from typing import List
from src.lexer.token_types import TokenType
from src.lexer.token import Token
from src.utils.error_handler import ParserError
from .ast_nodes import *


class Parser:
    """Parser for Bengali programming language."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def peek(self) -> Token:
        """Return current token without consuming it."""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Return the previously consumed token."""
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        """Check if we've reached the end of tokens."""
        return self.peek().type == TokenType.EOF

    def advance(self) -> Token:
        """Consume and return the current token."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def check(self, type_: TokenType) -> bool:
        """Check if current token is of given type without consuming."""
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def consume(self, type_: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error."""
        if self.check(type_):
            return self.advance()
        raise ParserError(message, self.peek().line, self.peek().column)

    def parse(self) -> Program:
        """Parse the complete program."""
        try:
            functions = []
            while not self.is_at_end():
                functions.append(self.parse_function())
            return Program(functions)
        except Exception as e:
            token = self.peek()
            raise ParserError(f"Unexpected error while parsing: {str(e)}",
                              token.line, token.column)

    def parse_function(self) -> FunctionDefinition:
        """Parse function definition."""
        is_main = self.peek().type == TokenType.MAIN
        if not (self.match(TokenType.FUNCTION) or self.match(TokenType.MAIN)):
            raise ParserError("Expected function declaration",
                              self.peek().line, self.peek().column)

        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        self.consume(TokenType.LPAREN, "Expected '(' after function name")

        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters = self.parse_parameter_list()

        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        body = self.parse_block()

        return FunctionDefinition(name, parameters, None, body, is_main)

    def parse_parameter_list(self) -> List[Parameter]:
        """Parse function parameters."""
        parameters = []

        while True:
            type_name = self.parse_type()
            name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
            parameters.append(Parameter(type_name, name))

            if not self.match(TokenType.COMMA):
                break

            if self.check(TokenType.RPAREN):
                raise ParserError("Expected parameter after comma",
                                  self.peek().line, self.peek().column)

        return parameters

    def parse_type(self) -> str:
        """Parse type declaration."""
        type_tokens = {
            TokenType.INTEGER: "সংখ্যা",
            TokenType.FLOAT: "দশমিক",
            TokenType.CHAR: "অক্ষর",
            TokenType.STRING: "কথা",
            TokenType.BOOLEAN: "সত্যমিথ্যা"
        }

        token = self.peek()
        if token.type in type_tokens:
            self.advance()
            return type_tokens[token.type]

        raise ParserError("Expected type declaration", token.line, token.column)

    def parse_block(self) -> Block:
        """Parse a block of statements."""
        self.consume(TokenType.LBRACE, "Expected '{' to begin block")
        statements = []

        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.parse_statement())

        self.consume(TokenType.RBRACE, "Expected '}' to end block")
        return Block(statements)

    def parse_statement(self) -> Statement:
        """Parse a single statement."""
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.check(TokenType.INTEGER) or self.check(TokenType.FLOAT) or \
                self.check(TokenType.CHAR) or self.check(TokenType.STRING) or \
                self.check(TokenType.BOOLEAN):
            return self.parse_variable_declaration()
        elif self.check(TokenType.IDENTIFIER):
            return self.parse_assignment_or_call()
        elif self.check(TokenType.LBRACE):
            return self.parse_block()
        else:
            raise ParserError("Expected statement",
                              self.peek().line, self.peek().column)

    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declaration."""
        type_name = self.parse_type()
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        initializer = None

        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VariableDeclaration(type_name, name, initializer)

    def parse_assignment_or_call(self) -> Statement:
        """Parse assignment or function call."""
        name = self.consume(TokenType.IDENTIFIER, "Expected identifier").value

        if self.match(TokenType.ASSIGN):
            value = self.parse_expression()
            self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
            return Assignment(name, value)
        elif self.match(TokenType.LPAREN):
            args = []
            if not self.check(TokenType.RPAREN):
                args = self.parse_arguments()

            self.consume(TokenType.RPAREN, "Expected ')' after function arguments")
            self.consume(TokenType.SEMICOLON, "Expected ';' after function call")
            return FunctionCall(name, args)
        else:
            raise ParserError("Expected '=' or '(' after identifier",
                              self.peek().line, self.peek().column)

    def parse_if_statement(self) -> IfStatement:
        """Parse if statement and optional else/elif blocks."""
        self.consume(TokenType.LPAREN, "Expected '(' after 'যদি'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after if condition")

        then_block = self.parse_block()
        else_block = None
        elif_blocks = []

        while self.match(TokenType.ELSE_IF):
            self.consume(TokenType.LPAREN, "Expected '(' after 'অথবা'")
            elif_condition = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after elif condition")
            elif_block = self.parse_block()
            elif_blocks.append((elif_condition, elif_block))

        if self.match(TokenType.ELSE):
            else_block = self.parse_block()

        return IfStatement(condition, then_block, else_block, elif_blocks)

    def parse_while_statement(self) -> WhileStatement:
        """Parse while statement."""
        self.consume(TokenType.LPAREN, "Expected '(' after 'যতক্ষণ'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after while condition")
        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_return_statement(self) -> ReturnStatement:
        """Parse return statement."""
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after return statement")
        return ReturnStatement(value)

    def parse_expression(self) -> Expression:
        """Parse expression."""
        return self.parse_assignment_expression()

    def parse_assignment_expression(self) -> Expression:
        """Parse assignment expression."""
        expr = self.parse_logical_or()

        if self.match(TokenType.ASSIGN):
            value = self.parse_assignment_expression()
            if not isinstance(expr, Identifier):
                raise ParserError("Invalid assignment target",
                                  self.previous().line, self.previous().column)
            return Assignment(expr.name, value)

        return expr

    def parse_logical_or(self) -> Expression:
        """Parse logical OR expression."""
        expr = self.parse_logical_and()

        while self.match(TokenType.OR):
            operator = self.previous().value
            right = self.parse_logical_and()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def parse_logical_and(self) -> Expression:
        """Parse logical AND expression."""
        expr = self.parse_equality()

        while self.match(TokenType.AND):
            operator = self.previous().value
            right = self.parse_equality()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def parse_equality(self) -> Expression:
        """Parse equality expression."""
        expr = self.parse_comparison()

        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous().value
            right = self.parse_comparison()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def parse_comparison(self) -> Expression:
        """Parse comparison expression."""
        expr = self.parse_addition()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous().value
            right = self.parse_addition()
            expr = BinaryOperation(expr, operator, right)

        return expr


