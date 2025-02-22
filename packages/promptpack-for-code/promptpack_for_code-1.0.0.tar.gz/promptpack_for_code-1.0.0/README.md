# promptpack-for-code

![PyPI](https://img.shields.io/pypi/v/promptpack-for-code.svg)

A command-line tool that bundles your code files into a single text file, optimized for AI code review and analysis. It helps developers prepare their codebase for productive conversations with AI language models by combining multiple source files into a well-formatted context.

## Installation

```bash
pip install promptpack-for-code
```

## Usage

Basic usage with a single directory:
```bash
promptpack-for-code /path/to/your/code
```

Process multiple directories:
```bash
promptpack-for-code dir1 dir2 dir3
```

Specify root directory for tree structure and full relative paths:
```bash
promptpack-for-code /path/to/specific/folder -r /path/to/project/root
```

Specify output file path:
```bash
promptpack-for-code /path/to/src -o /path/to/output/result.txt
```

Ignore specific patterns:
```bash
promptpack-for-code /path/to/src --ignore "*.log" "*.tmp"
```

Show progress bar during processing:
```bash
promptpack-for-code /path/to/src --progress
```

Force overwrite existing output file:
```bash
promptpack-for-code /path/to/src -f
```

## Features

- Combines multiple source files from one or more directories into a single output file
- Generates a tree-like directory structure based on the specified root
- Preserves file structure with full relative paths from the root directory
- Built-in ignore patterns for common files (e.g., `.git`, `__pycache__`, etc.)
- Customizable output file path
- Optional progress bar for large projects
- Easy to integrate with various AI chat platforms

## Output Format

The generated output file contains:
1. A tree-like representation of your project structure (based on the root directory)
2. The contents of all files in the specified directories, with paths relative to the root

Example output:
```
Project Directory Structure:
==========================
project-name
├── src
│   ├── main.py
│   └── utils
│       └── helper.py
└── tests
    └── test_main.py

File Contents from Selected Directories:
===================================

====
File: src/main.py
----
[file content here]

====
File: src/utils/helper.py
----
[file content here]

====
File: tests/test_main.py
----
[file content here]
```

## Development

To contribute to this project:

1. Clone the repository:
```bash
git clone https://github.com/changyy/py-promptpack-for-code.git
cd py-promptpack-for-code
```

2. Install in development mode:
```bash
pip install -e .
```

## Requirements

- Python 3.6+
- tqdm (for progress bar support)

## License

MIT License - see LICENSE file for details
