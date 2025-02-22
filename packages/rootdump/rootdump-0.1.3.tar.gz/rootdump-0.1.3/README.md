# rootdump

[![PyPI version](https://badge.fury.io/py/rootdump.svg)](https://badge.fury.io/py/rootdump)
[![Python Versions](https://img.shields.io/pypi/pyversions/rootdump.svg)](https://pypi.org/project/rootdump/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for dumping directory contents into a single organized text file. Perfect for code reviews, documentation, and project analysis.

## Features

✨ **Tree Structure** - Displays directory structure in a tree format  
📝 **Content Dump** - Dumps the content of all text files  
🔍 **Extension Filtering** - Filter files by extension  
⚡ **Binary Detection** - Automatically excludes binary files  
🔢 **Line Numbers** - Includes line numbers with a separator for easy reading.

## Installation

```bash
pip install rootdump
```

## Quick Start

### Command Line Usage

Basic usage:
```bash
rootdump /path/to/source output.txt
```

With options:
```bash
# Exclude binary files
rootdump /path/to/source output.txt --exclude-binary

# Include only specific extensions
rootdump /path/to/source output.txt --extensions .py .txt .md

# Skip directory tree structure
rootdump /path/to/source output.txt --no-tree

# Exclude line numbers from the output
rootdump /path/to/source output.txt --no-line-numbers
```

### Python API

```python
from rootdump import dump_directory

# Basic usage
dump_directory("source_dir", "output.txt")

# With options
dump_directory(
    "source_dir",
    "output.txt",
    exclude_binary=True,
    include_extensions=[".py", ".txt"],
    show_tree=True,
    show_line_numbers=True
)
```

## Output Example

```
# Directory structure:
# .
# ├── src/
# │   ├── __init__.py
# │   └── main.py
# ├── tests/
# │   └── test_main.py
# └── README.md

## src/__init__.py

1 | def hello():
2 |     print("Hello from src/__init__.py")

## src/main.py

1 | def main():
2 |     print("Hello from src/main.py")
3 |
4 | if __name__ == "__main__":
5 |     main()
```

## Contributing

Contributions are welcome! Feel free to:

- Report issues
- Suggest features
- Submit pull requests

## Acknowledgments

This project was inspired by [uithub.com](https://uithub.com)'s project structure visualization.

## License

This project is licensed under the MIT License - see the LICENSE file for details.