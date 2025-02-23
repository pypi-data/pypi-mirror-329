# JsonGeekAI

[![PyPI version](https://img.shields.io/pypi/v/jsongeekai.svg)](https://pypi.org/project/jsongeekai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/jsongeekai.svg)](https://pypi.org/project/jsongeekai/)
[![Downloads](https://img.shields.io/pypi/dm/jsongeekai.svg)](https://pypi.org/project/jsongeekai/)
[![Tests](https://img.shields.io/github/workflow/status/zhanghongping/jsongeekai/Tests)](https://github.com/zhanghongping/jsongeekai/actions)
[![Coverage Status](https://coveralls.io/repos/github/zhanghongping/jsongeekai/badge.svg?branch=main)](https://coveralls.io/github/zhanghongping/jsongeekai?branch=main)
[![License](https://img.shields.io/pypi/l/jsongeekai.svg)](https://github.com/zhanghongping/jsongeekai/blob/main/LICENSE)

A high-performance JSON parser with AI-driven optimizations and multi-format support.

## Features

- **SIMD Optimizations**: Utilizes SIMD instructions for faster parsing when available
- **Multi-format Support**: Handles JSON, JSON5, YAML, MessagePack, and JSONL formats
- **Memory Efficient**: Smart memory management with configurable limits
- **Format Auto-detection**: Automatically detects and handles different formats
- **Rich Error Handling**: Detailed error messages with context and documentation
- **Compression Support**: Built-in compression for JSONL format
- **Extensible**: Easy to add new formats and optimizations
- **Well Tested**: Comprehensive test suite with performance benchmarks

## Installation

```bash
pip install jsongeekai
```

## Quick Start

```python
from jsongeekai import JsonGeekAI

# Create parser
parser = JsonGeekAI()

# Parse JSON
data = parser.parse('{"name": "JsonGeekAI", "version": "0.2.0"}')

# Use different formats
from jsongeekai.formats import FormatHandler

handler = FormatHandler()

# Auto-detect and parse
data = handler.parse(content)

# Specific format
data = handler.parse_json5(content)
data = handler.parse_yaml(content)
data = handler.parse_msgpack(content)

# With memory limits
parser = JsonGeekAI(memory_limit=1024*1024)  # 1MB limit
```

## Version Compatibility

JsonGeekAI requires Python 3.8 or later and is tested on:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## Performance

JsonGeekAI is designed for performance:

- SIMD acceleration when available
- Efficient memory usage
- Format-specific optimizations
- Streaming support for large files

## Documentation

Full documentation is available at [jsongeekai.readthedocs.io](https://jsongeekai.readthedocs.io/)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

JsonGeekAI is released under the MIT License. See the [LICENSE](LICENSE) file for details.
