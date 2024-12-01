import sys

from wangs_algorithm import Operator, Statement

def check_and_parse_input(input: str) -> tuple[Statement, Statement]:
    stack: list = list()
    l: int = len(input)
    has_rightarrow: bool = False
    left_statement: Statement
    right_statement: Statement
    left_paren_cnt: int = 0
    i: int = 0
    while i < l:
        if input[i].isupper():
            if stack and isinstance(stack[-1], Statement):
                format_error()
            new_statement: Statement = Statement()
            new_statement.content = input[i]
            if stack and stack[-1] == Operator.NOT:
                stack.pop()
                new_statement.is_not = True
            stack.append(new_statement)
            i += 1
        elif input[i] == "!":
            if stack and (isinstance(stack[-1], Statement) or stack[-1] == Operator.NOT):
                format_error()
            stack.append(Operator.NOT)
            i += 1
        elif input[i] == "(":
            if stack and isinstance(stack[-1], Statement):
                format_error()
            stack.append("(")
            left_paren_cnt += 1
            i += 1
        elif input[i] == ")":
            if stack and isinstance(stack[-1], Operator):
                format_error()
            statement_cnt: int = 0
            new_statement = Statement()
            has_left_paren: bool = False
            type_operator: Operator
            sub_stack: list = list()
            while stack:
                obj = stack.pop()
                if obj == "(":
                    has_left_paren = True
                    break
                elif isinstance(obj, Statement):
                    sub_stack.append(obj)
                    statement_cnt += 1
                elif statement_cnt == 1:
                    sub_stack.append(obj)
                    type_operator = obj
                elif obj != type_operator:
                    format_error()
                else:
                    sub_stack.append(obj)
            if statement_cnt < 2 or not has_left_paren:
                format_error()
            if statement_cnt > 2 and (type_operator == Operator.RIGHTARROW or type_operator == Operator.LEFTRIGHTARROW):
                format_error()
            while sub_stack:
                new_statement.sub_statements.append(sub_stack.pop())
            new_statement.is_single = False
            new_statement.optr_type = type_operator
            if stack and stack[-1] == Operator.NOT:
                stack.pop()
                new_statement.is_not = True
            stack.append(new_statement)
            left_paren_cnt -= 1
            i += 1
        elif input[i] == "\\":
            if stack and (isinstance(stack[-1], Operator) or stack[-1] == "("):
                format_error()
            if i < l - 2 and input[i + 1] == "/":
                stack.append(Operator.VEE)
                i += 2
            else:
                format_error()
        elif input[i] == "/":
            if stack and (isinstance(stack[-1], Operator) or stack[-1] == "("):
                format_error()
            if i < l - 2 and input[i + 1] == "\\":
                stack.append(Operator.WEDGE)
                i += 2
            else:
                format_error()
        elif input[i] == "<":
            if stack and (isinstance(stack[-1], Operator) or stack[-1] == "("):
                format_error()
            if i < l - 3 and input[i + 1] == "-" and input[i + 2] == ">":
                stack.append(Operator.LEFTRIGHTARROW)
                i += 3
            else:
                format_error()
        elif input[i] == "-":
            if left_paren_cnt == 0:
                if not has_rightarrow and len(stack) == 1 and isinstance(stack[0], Statement):
                    if i < l - 2 and input[i + 1] == ">":
                        has_rightarrow = True
                        left_statement = stack.pop()
                        i += 2
                    else:
                        format_error()
                else:
                    format_error()
            else:
                if stack and (isinstance(stack[-1], Operator) or stack[-1] == "("):
                    format_error()
                if i < l - 2 and input[i + 1] == ">":
                    stack.append(Operator.RIGHTARROW)
                    i += 2
                else:
                    format_error()
    if has_rightarrow and left_paren_cnt == 0 and len(stack) == 1 and isinstance(stack[0], Statement):
        right_statement = stack.pop()
    else:
        format_error()
    return (left_statement, right_statement)


def format_error() -> None:
    print("Input format error. Please check the usage.")
    sys.exit(1)
