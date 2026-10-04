# Build Specification for app.py - Addition App

## Program Overview
The addition app is a Python command-line application that performs addition operations between two numerical inputs provided by the user. It validates the input to ensure they are numbers (integers or floats) and returns the sum. The application should gracefully handle invalid inputs and display appropriate error messages.

## Public Functions

### 1. Function: `add_numbers(num1: float, num2: float) -> float`
- **Description**: Takes two numbers as input and returns their sum.
- **Parameters**:
  - `num1`: A float representing the first number to be added.
  - `num2`: A float representing the second number to be added.
- **Return Value**: A float representing the sum of `num1` and `num2`.

### 2. Function: `validate_input(input_str: str) -> float`
- **Description**: Validates if the input string can be converted into a float.
- **Parameters**:
  - `input_str`: A string that needs to be validated and converted.
- **Return Value**: A float if the input string is valid, raises a `ValueError` if invalid.

### 3. Function: `main() -> None`
- **Description**: The main function which serves as the entry point of the application. It prompts users for input, calls the necessary functions to validate and compute the sum, and prints the results.
- **Parameters**: None
- **Return Value**: None

## Acceptance Cases

### Test Case 1: Valid Inputs (Integer Addition)
- **Input**: 
  - User inputs: `3` and `5`
- **Expected Output**: 
  - `8.0` (sum of 3 and 5)

### Test Case 2: Valid Inputs (Float Addition)
- **Input**: 
  - User inputs: `3.5` and `2.1`
- **Expected Output**: 
  - `5.6` (sum of 3.5 and 2.1)

### Test Case 3: Valid Inputs (Mixed Types)
- **Input**: 
  - User inputs: `4` and `6.5`
- **Expected Output**: 
  - `10.5` (sum of 4 and 6.5)

### Test Case 4: Invalid Input (Non-numeric)
- **Input**: 
  - User inputs: `"abc"` and `5`
- **Expected Output**: 
  - Error Message: `"Invalid input. Please enter numeric values."` 

### Test Case 5: Edge Case (Empty Input)
- **Input**: 
  - User inputs: `""` (empty string) and `5`
- **Expected Output**: 
  - Error Message: `"Invalid input. Please enter numeric values."` 

### Test Case 6: Invalid Input (Special Characters)
- **Input**: 
  - User inputs: `$100` and `50`
- **Expected Output**: 
  - Error Message: `"Invalid input. Please enter numeric values."` 

### Test Case 7: Valid Inputs (Negative Numbers)
- **Input**: 
  - User inputs: `-7` and `-3`
- **Expected Output**: 
  - `-10.0` (sum of -7 and -3)

### Test Case 8: Valid Inputs (Zero)
- **Input**: 
  - User inputs: `0` and `5`
- **Expected Output**: 
  - `5.0` (sum of 0 and 5)

This specification provides a comprehensive framework for implementing the addition app in a single Python module named `app.py`, ensuring that it handles various cases, including valid calculations and edge case scenarios.
