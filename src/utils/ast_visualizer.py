from src.parser.ast_nodes import *
from typing import Any


class ASTVisualizer:
    def __init__(self):
        self.indent_level = 0
        self.indent_size = 2

    def visit(self, node: Any) -> str:
        method_name = f'visit_{node.__class__.__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: Any) -> str:
        return f"{' ' * self.indent_level}Node: {node.__class__.__name__}"

    def indent(self):
        self.indent_level += self.indent_size

    def dedent(self):
        self.indent_level -= self.indent_size

    def visit_Program(self, node: Program) -> str:
        result = "Program\n"
        self.indent()
        for function in node.functions:
            result += self.visit(function) + "\n"
        self.dedent()
        return result

    def visit_FunctionDefinition(self, node: FunctionDefinition) -> str:
        result = f"{' ' * self.indent_level}Function: {node.name} (Main: {node.is_main})\n"
        self.indent()

        if node.parameters:
            result += f"{' ' * self.indent_level}Parameters:\n"
            self.indent()
            for param in node.parameters:
                result += self.visit(param) + "\n"
            self.dedent()

        result += self.visit(node.body)
        self.dedent()
        return result

    def visit_Parameter(self, node: Parameter) -> str:
        return f"{' ' * self.indent_level}{node.name}: {node.type_name}"

    def visit_Block(self, node: Block) -> str:
        result = f"{' ' * self.indent_level}Block:\n"
        self.indent()
        for statement in node.statements:
            result += self.visit(statement) + "\n"
        self.dedent()
        return result

    def visit_VariableDeclaration(self, node: VariableDeclaration) -> str:
        result = f"{' ' * self.indent_level}VarDecl: {node.name} ({node.type_name})"
        if node.initializer:
            result += " =\n"
            self.indent()
            result += self.visit(node.initializer)
            self.dedent()
        return result

    def visit_Assignment(self, node: Assignment) -> str:
        result = f"{' ' * self.indent_level}Assign: {node.target} =\n"
        self.indent()
        result += self.visit(node.value)
        self.dedent()
        return result

    def visit_IfStatement(self, node: IfStatement) -> str:
        result = f"{' ' * self.indent_level}If:\n"
        self.indent()
        result += f"{' ' * self.indent_level}Condition:\n"
        self.indent()
        result += self.visit(node.condition) + "\n"
        self.dedent()
        result += f"{' ' * self.indent_level}Then:\n"
        result += self.visit(node.then_block) + "\n"

        for condition, block in node.elif_blocks:
            result += f"{' ' * self.indent_level}Elif:\n"
            self.indent()
            result += f"{' ' * self.indent_level}Condition:\n"
            self.indent()
            result += self.visit(condition) + "\n"
            self.dedent()
            result += f"{' ' * self.indent_level}Block:\n"
            result += self.visit(block) + "\n"
            self.dedent()

        if node.else_block:
            result += f"{' ' * self.indent_level}Else:\n"
            result += self.visit(node.else_block)
        self.dedent()
        return result

    def visit_WhileStatement(self, node: WhileStatement) -> str:
        result = f"{' ' * self.indent_level}While:\n"
        self.indent()
        result += f"{' ' * self.indent_level}Condition:\n"
        self.indent()
        result += self.visit(node.condition) + "\n"
        self.dedent()
        result += f"{' ' * self.indent_level}Body:\n"
        result += self.visit(node.body)
        self.dedent()
        return result

    def visit_ReturnStatement(self, node: ReturnStatement) -> str:
        result = f"{' ' * self.indent_level}Return"
        if node.value:
            result += ":\n"
            self.indent()
            result += self.visit(node.value)
            self.dedent()
        return result

    def visit_BinaryOperation(self, node: BinaryOperation) -> str:
        result = f"{' ' * self.indent_level}BinaryOp: {node.operator}\n"
        self.indent()
        result += f"{' ' * self.indent_level}Left:\n"
        self.indent()
        result += self.visit(node.left) + "\n"
        self.dedent()
        result += f"{' ' * self.indent_level}Right:\n"
        self.indent()
        result += self.visit(node.right)
        self.dedent()
        self.dedent()
        return result

    def visit_UnaryOperation(self, node: UnaryOperation) -> str:
        result = f"{' ' * self.indent_level}UnaryOp: {node.operator}\n"
        self.indent()
        result += self.visit(node.operand)
        self.dedent()
        return result

    def visit_Literal(self, node: Literal) -> str:
        return f"{' ' * self.indent_level}Literal: {node.value} ({node.type_name})"

    def visit_Identifier(self, node: Identifier) -> str:
        return f"{' ' * self.indent_level}Identifier: {node.name}"

    def visit_FunctionCall(self, node: FunctionCall) -> str:
        result = f"{' ' * self.indent_level}FunctionCall: {node.name}\n"
        if node.arguments:
            self.indent()
            result += f"{' ' * self.indent_level}Arguments:\n"
            self.indent()
            for arg in node.arguments:
                result += self.visit(arg) + "\n"
            self.dedent()
            self.dedent()
        return result