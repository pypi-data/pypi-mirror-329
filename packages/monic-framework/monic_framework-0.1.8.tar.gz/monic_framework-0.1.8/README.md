# Monic Framework

<p>
<a href="https://codecov.io/gh/cognica-io/monic-framework" target="_blank"><img src="https://img.shields.io/codecov/c/github/cognica-io/monic-framework?color=%2334D058" alt="Code coverage"></a>
<a href="https://pypi.org/project/monic-framework" target="_blank"><img src="https://img.shields.io/pypi/v/monic-framework?color=%2334D058" alt="Package version"></a>
<a href="https://pypi.org/project/monic-framework" target="_blank"><img src="https://img.shields.io/pypi/pyversions/monic-framework" alt="Supported Python versions"></a>
<a href="https://pypi.org/project/monic-framework" target="_blank"><img src="https://img.shields.io/pypi/dm/monic-framework?color=%2334D058" alt="PyPI - Downloads"></a>
<a href="https://pypi.org/project/monic-framework" target="_blank"><img src="https://img.shields.io/pypi/l/monic-framework?color=%2334D058" alt="PyPI - License"></a>
</p>

Monic Framework is a powerful expression evaluation and code execution framework that provides a safe and flexible way to parse and interpret Python-style code. It offers a robust expression parser and interpreter designed for dynamic code evaluation, scripting, and embedded programming scenarios.

## Key Features

- Python-style syntax support
- Secure code execution environment
- Expression parsing and interpretation
- Function definition and call support
- Built-in type checking and validation
- Seamless integration with existing Python projects

## Supported Language Features

### Core Python Features

- Variables and basic data types (int, float, str, bool, etc.)
- Control flow statements (if/else, for, while, break, continue)
- Functions with full parameter support:
  - Positional and keyword arguments
  - Default values
  - Variable arguments (*args)
  - Keyword arguments (**kwargs)
  - Keyword-only arguments
- Lambda expressions
- List, set, and dictionary comprehensions
- Context managers (with statements)
- Exception handling (try/except/finally)
- Classes and object-oriented programming
- Pattern matching (match/case statements)

### Expression Support

- Arithmetic operations (+, -, *, /, //, %, **)
- Comparison operations (==, !=, <, >, <=, >=)
- Logical operations (and, or, not)
- Bitwise operations (&, |, ^, <<, >>)
- Assignment operations (=, +=, -=, *=, etc.)
- Attribute access (obj.attr)
- Subscript operations (obj[key])
- Function and method calls
- String formatting (f-strings)
- Tuple and list unpacking
- Named expressions (walrus operator :=)

### Built-in Functions and Types

- Essential built-ins (print, len, range, etc.)
- Type conversion functions (int, float, str, bool)
- Collection operations (min, max, sum, sorted)
- Iteration helpers (enumerate, zip, filter, map)
- Type checking (isinstance, issubclass)

### Security Features

- Sandboxed execution environment
- Restricted access to system resources
- Prevention of malicious code execution
- Execution timeout protection:
  - Configurable maximum execution time
  - Automatic termination of long-running code
  - Protection against infinite loops
  - Time-based resource control
- Forbidden operations disallowed:
  - File system operations
  - System command execution
  - Module imports
  - Access to sensitive attributes
  - Dangerous built-in functions

## Installation

### Basic Installation

```bash
pip install -U monic-framework
```

Or with extra dependencies such as `pyarrow`, `numpy`, `pandas`, and `polars`:

```bash
pip install -U monic-framework[extra]
```

### Development Installation

```bash
pip install -e .[dev]
```

Or with extra dependencies such as `pyarrow`, `numpy`, `pandas`, and `polars`:

```bash
pip install -e .[dev,extra]
```

## Quick Start

### Basic Usage

```python
from monic.expressions import ExpressionsParser, ExpressionsInterpreter


# Initialize parser and interpreter
parser = ExpressionsParser()
interpreter = ExpressionsInterpreter()

# Define code to execute
code = """
# Variable assignment
x = 10
y = 20

# Conditional statement
if x < y:
    result = "y is greater"
else:
    result = "x is greater"

# Return result
result
"""

# Parse code and execute it
tree = parser.parse(code)
result = interpreter.execute(tree)
print(result)  # Output: "y is greater"
```

### Function Definition and Calls

```python
from monic.expressions import ExpressionsParser, ExpressionsInterpreter


# Initialize parser and interpreter
parser = ExpressionsParser()
interpreter = ExpressionsInterpreter()

# Define code to execute
code = """
def calculate_sum(a: int, b: int) -> int:
    return a + b

def calculate_average(numbers: list[int]) -> float:
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Using functions
sum_result = calculate_sum(10, 20)
avg_result = calculate_average([1, 2, 3, 4, 5])

[sum_result, avg_result]
"""

# Parse code and execute it
tree = parser.parse(code)
result = interpreter.execute(tree)
print(result)  # Output: [30, 3.0]
```

### Binding Python Objects

```python
from monic.expressions import (
    ExpressionsParser,
    ExpressionsInterpreter,
    monic_bind,
)


# Define functions and bind them to the interpreter
@monic_bind
def calculate_sum(x: int, y: int) -> int:
    return x + y


@monic_bind
def calculate_average(numbers: list[int]) -> float:
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


# Initialize parser and interpreter
parser = ExpressionsParser()
interpreter = ExpressionsInterpreter()

# Define code to execute
code = """
# Using bound functions
sum_result = calculate_sum(10, 20)
avg_result = calculate_average([1, 2, 3, 4, 5])

[sum_result, avg_result]
"""

# Parse code and execute it
tree = parser.parse(code)
result = interpreter.execute(tree)
print(result)  # Output: [30, 3.0]
```

### Timeout Control

```python
from monic.expressions import ExpressionsParser, ExpressionsContext, ExpressionsInterpreter


# Initialize parser
parser = ExpressionsParser()
# Initialize with timeout context
context = ExpressionsContext(timeout=5.0)  # Set 5 seconds timeout
# Initialize interpreter with context
interpreter = ExpressionsInterpreter(context=context)

# This will be terminated after 5 seconds
code = """
while True:
    pass  # Infinite loop
"""

try:
    tree = parser.parse(code)
    interpreter.execute(tree)
except TimeoutError:
    print("Code execution timed out")  # Output: Code execution timed out
```

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Issues and Support

For bug reports or feature requests, please submit them through GitHub Issues.
