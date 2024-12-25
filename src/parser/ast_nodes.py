from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class Node:
    pass

@dataclass
class Program(Node):
    functions: List['FunctionDefinition']

@dataclass
class FunctionDefinition(Node):
    name: str
    parameters: List['Parameter']
    return_type: Optional[str]
    body: 'Block'
    is_main: bool

@dataclass
class Parameter(Node):
    type_name: str
    name: str

@dataclass
class Block(Node):
    statements: List['Statement']

@dataclass
class Statement(Node):
    pass

@dataclass
class VariableDeclaration(Statement):
    type_name: str
    name: str
    initializer: Optional['Expression']

@dataclass
class Assignment(Statement):
    target: str
    value: 'Expression'

@dataclass
class IfStatement(Statement):
    condition: 'Expression'
    then_block: Block
    else_block: Optional[Block]
    elif_blocks: List[tuple['Expression', Block]]

@dataclass
class WhileStatement(Statement):
    condition: 'Expression'
    body: Block

@dataclass
class ReturnStatement(Statement):
    value: Optional['Expression']

@dataclass
class Expression(Node):
    pass

@dataclass
class BinaryOperation(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOperation(Expression):
    operator: str
    operand: Expression

@dataclass
class Literal(Expression):
    value: Union[int, float, str, bool]
    type_name: str

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]