from enum import Enum

class Operator(Enum):
    NOT = 1
    WEDGE = 2
    VEE = 3
    RIGHTARROW = 4
    LEFTRIGHTARROW = 5
    DEFAULT = 6

class Statement:
    def __init__(self) -> None:
        self.is_not: bool = False
        self.is_single: bool = True
        self.optr_type: Operator = Operator.DEFAULT
        self.content: str = ""
        self.sub_statements: list = list()
