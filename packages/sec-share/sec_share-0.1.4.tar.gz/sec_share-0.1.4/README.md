# SecShare

A command-line tool for securely sharing code snippets with automatic secret detection and redaction.

## Installation

```bash
pip install sec-share
```

## Usage

```bash
# Share a file
sec-share -t "My Code" -l language my_script

# Share from stdin
cat my_script.py | sec-share -t "My Code" -l python
```

## Features

- Automatic detection and redaction of sensitive information
- Support for multiple programming languages
- Secure sharing with expiration dates
- Easy-to-use command-line interface

## License

MIT License
