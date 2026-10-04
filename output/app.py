def add_numbers(num1: float, num2: float) -> float:
    return num1 + num2


def validate_input(input_str: str) -> float:
    try:
        return float(input_str)
    except ValueError:
        raise ValueError("Invalid input. Please enter numeric values.")


def main() -> None:
    try:
        num1_str = input("Enter the first number: ")
        num1 = validate_input(num1_str)
        num2_str = input("Enter the second number: ")
        num2 = validate_input(num2_str)
        result = add_numbers(num1, num2)
        print(result)
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()