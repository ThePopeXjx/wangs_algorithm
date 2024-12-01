import argparse

from wangs_algorithm import Statement, check_and_parse_input, deduction

def main():
    parser = argparse.ArgumentParser(prog="test")
    parser.add_argument('--showsteps', action="store_true", required=False)
    args = parser.parse_args()
    input_statement: str = input("Please enter your statement: ")
    s: tuple[Statement, Statement] = check_and_parse_input(input_statement)
    deduction(s, args.showsteps)

if __name__ == "__main__":
    main()
