# ezDebugger

A lightweight Python debugging toolkit providing decorator-based function call tracing and logging.

## Features

- **Function Tracing**: Automatic logging of function calls with parameters
- **Flexible Debugging**: Turn debugging on/off dynamically
- **Debug Levels**: Control verbosity with different debug levels
- **Minimal Overhead**: Lightweight decorator implementation with no external dependencies
- **Class-aware**: Distinguishes between class methods and module functions

## Installation

Install from PyPI:

```bash
pip install ezDebugger
```

## Quick Start

```python
from ezDebugger import Logger

@Logger
def my_function(x, y):
    return x + y

# Enable debugging
my_function.active = True
result = my_function(5, 3)

# Output:
# DEBUG: Function Running: my_function()
#     | LOCALE -> your_file.py
#     | PARAMS -> (5, 3)
#     ‾
```

## Usage

### Basic Decorator

Use the `@Logger` decorator on any function:

```python
from ezDebugger import Logger

@Logger
def calculate(a, b):
    return a * b
```

### Controlling Debug Output

```python
# Enable/disable debugging
calculate.active = True
calculate.active = False

# Set debug level (controls which functions are shown)
calculate.lvl = 1  # Show all functions
calculate.lvl = 2  # Hide private functions (starting with _)
```

### With Classes

The logger automatically detects class methods and includes class information:

```python
class Calculator:
    @Logger
    def add(self, x, y):
        return x + y

calc = Calculator()
calc.add(5, 3)
# DEBUG: Function Running: Calculator.add()
#     | LOCALE -> your_file.py
#     | PARAMS -> (5, 3)
#     ‾
```

## API Reference

### Logger

A decorator class for tracing function execution.

**Attributes:**
- `active` (bool): Enable/disable debug output (default: `True`)
- `lvl` (int): Debug verbosity level (default: `1`)
  - Level 1: Show all functions
  - Level 2+: Hide private functions (starting with `_`)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
