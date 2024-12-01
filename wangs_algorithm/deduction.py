import copy

from wangs_algorithm import Statement, Operator

def deduction(initial_statements: tuple[Statement, Statement], show_deduction_steps: bool) -> None:
    if show_deduction_steps:
        print("Deduction starts.\n")
    statements_groups: list[list[list[Statement]]] = []
    left_init_statements: list[Statement] = []
    right_init_statements: list[Statement] = []
    if initial_statements[0].is_single or initial_statements[0].optr_type != Operator.WEDGE:
        left_init_statements.append(initial_statements[0])
    else:
        for item in initial_statements[0].sub_statements:
            if isinstance(item, Statement):
                left_init_statements.append(item)
    if initial_statements[1].is_single or initial_statements[1].optr_type != Operator.VEE:
        right_init_statements.append(initial_statements[1])
    else:
        for item in initial_statements[1].sub_statements:
            if isinstance(item, Statement):
                right_init_statements.append(item)
    statements_groups.append([left_init_statements, right_init_statements])
    if show_deduction_steps:
        print("Step 1:")
        print_statements_group(statements_groups)
        print()
    n_steps: int = 2
    deduction_done = False
    while not deduction_done:
        deduction_done = True
        n_groups: int = len(statements_groups)
        for i in range(n_groups):
            n_left_statements: int = len(statements_groups[i][0])
            n_right_statements: int = len(statements_groups[i][1])
            for j in range(n_left_statements):
                if statements_groups[i][0][j].is_not:
                    deduction_done = False
                    statements_groups[i][0][j].is_not = False
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[1].append(copy.deepcopy(statements_groups[i][0][j]))
                    statements_groups.append(tmp)
                    del statements_groups[i]
                    break
                if statements_groups[i][0][j].optr_type == Operator.WEDGE:
                    deduction_done = False
                    for item in statements_groups[i][0][j].sub_statements:
                        if isinstance(item, Statement):
                            statements_groups[i][0].append(copy.deepcopy(item))
                    del statements_groups[i][0][j]
                    break
                if statements_groups[i][0][j].optr_type == Operator.VEE:
                    deduction_done = False
                    for item in statements_groups[i][0][j].sub_statements:
                        if isinstance(item, Statement):
                            tmp = copy.deepcopy(statements_groups[i])
                            del tmp[0][j]
                            tmp[0].append(copy.deepcopy(item))
                            statements_groups.append(tmp)
                    del statements_groups[i]
                    break
                if statements_groups[i][0][j].optr_type == Operator.RIGHTARROW:
                    deduction_done = False
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[0].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[2]))
                    statements_groups.append(tmp)
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[1].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[0]))
                    statements_groups.append(tmp)
                    del statements_groups[i]
                    break
                if statements_groups[i][0][j].optr_type == Operator.LEFTRIGHTARROW:
                    deduction_done = False
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[0].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[0]))
                    tmp[0].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[2]))
                    statements_groups.append(tmp)
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[1].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[0]))
                    tmp[1].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[2]))
                    statements_groups.append(tmp)
                    del statements_groups[i]
                    break
            if not deduction_done:
                break
            for j in range(n_right_statements):
                if statements_groups[i][1][j].is_not:
                    deduction_done = False
                    statements_groups[i][1][j].is_not = False
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[1][j]
                    tmp[0].append(copy.deepcopy(statements_groups[i][1][j]))
                    statements_groups.append(tmp)
                    del statements_groups[i]
                    break
                if statements_groups[i][1][j].optr_type == Operator.WEDGE:
                    deduction_done = False
                    for item in statements_groups[i][1][j].sub_statements:
                        if isinstance(item, Statement):
                            tmp = copy.deepcopy(statements_groups[i])
                            del tmp[1][j]
                            tmp[1].append(copy.deepcopy(item))
                            statements_groups.append(tmp)
                    del statements_groups[i]
                    break
                if statements_groups[i][1][j].optr_type == Operator.VEE:
                    deduction_done = False
                    for item in statements_groups[i][1][j].sub_statements:
                        if isinstance(item, Statement):
                            statements_groups[i][1].append(copy.deepcopy(item))
                    del statements_groups[i][1][j]
                    break
                if statements_groups[i][1][j].optr_type == Operator.RIGHTARROW:
                    deduction_done = False
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[1][j]
                    tmp[0].append(copy.deepcopy(statements_groups[i][1][j].sub_statements[0]))
                    tmp[1].append(copy.deepcopy(statements_groups[i][1][j].sub_statements[2]))
                    statements_groups.append(tmp)
                    del statements_groups[i]
                    break
                if statements_groups[i][1][j].optr_type == Operator.LEFTRIGHTARROW:
                    deduction_done = False
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[0].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[0]))
                    tmp[1].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[2]))
                    statements_groups.append(tmp)
                    tmp = copy.deepcopy(statements_groups[i])
                    del tmp[0][j]
                    tmp[0].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[2]))
                    tmp[1].append(copy.deepcopy(statements_groups[i][0][j].sub_statements[0]))
                    statements_groups.append(tmp)
                    del statements_groups[i]
                    break
            if not deduction_done:
                break
        if not deduction_done:
            if show_deduction_steps:
                print(f"Step {n_steps}:")
                print_statements_group(statements_groups)
                print()
                n_steps += 1
    for statements_group in statements_groups:
        if not check_statements_group(statements_group):
            print("Unproved!")
            return
    print("Proved!")
    return

def print_statements_group(statements_groups: list[list[list[Statement]]]) -> None:
    for statements_group in statements_groups:
        for i, statement in enumerate(statements_group[0]):
            if i > 0:
                print(", ", end="")
            print_statement(statement)
        print(" => ", end="")
        for i, statement in enumerate(statements_group[1]):
            if i > 0:
                print(", ", end="")
            print_statement(statement)
        print()

def print_statement(statement: Statement) -> None:
    if statement.is_not:
        print("!", end="")
    if not statement.is_single:
        print("(", end="")
        for item in statement.sub_statements:
            if isinstance(item, Statement):
                print_statement(item)
            elif item == Operator.VEE:
                print("\\/", end="")
            elif item == Operator.WEDGE:
                print("/\\", end="")
            elif item == Operator.RIGHTARROW:
                print("->", end="")
        print(")", end="")
    else:
        print(f"{statement.content}", end="")

def check_statements_group(statements_group: list[list[Statement]]) -> bool:
    for left_item in statements_group[0]:
        for right_item in statements_group[1]:
            if left_item.content == right_item.content:
                return True
    return False
