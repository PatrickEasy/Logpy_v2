# Logpy_v2

A reusable Python logging utility library designed to provide consistent, structured logging across multiple projects.

## Overview

Logpy_v2 is a lightweight logging framework that can be easily integrated into your Python projects. It provides a standardized approach to logging with customizable formatters, handlers, and log levels.

## Features

- **Easy Integration**: Simple setup with minimal configuration
- **Structured Logging**: Consistent log format across all your projects
- **Flexible Configuration**: Customizable log levels, formats, and output destinations
- **Multiple Handlers**: Support for console, file, and rotating file handlers
- **Production Ready**: Designed for use in production environments

## Installation

### From Source

```bash
git clone https://github.com/PatrickEasy/Logpy_v2.git
cd Logpy_v2
pip install -r requirements.txt
```

### As a Git Submodule (Recommended for personal projects)

```bash
cd your-project
git submodule add https://github.com/PatrickEasy/Logpy_v2.git
pip install -r Logpy_v2/requirements.txt
```

## Quick Start

```python
from logpy_v2 import Logger

# Initialize logger
logger = Logger(name="my_app")

# Log messages
logger.info("Application started")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical issue")
```

## Configuration

### Basic Configuration

```python
from logpy_v2 import Logger

logger = Logger(
    name="my_app",
    level="INFO",
    log_file="app.log"
)
```

### Advanced Configuration

```python
from logpy_v2 import Logger

logger = Logger(
    name="my_app",
    level="DEBUG",
    log_file="app.log",
    max_bytes=10485760,  # 10MB
    backup_count=5,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## Usage in Multiple Projects

Since this is designed as a reusable library for your personal projects, here are recommended approaches:

### Option 1: Git Submodule
Add this repository as a submodule to your other projects:
```bash
git submodule add https://github.com/PatrickEasy/Logpy_v2.git
```

### Option 2: Local Package Installation
Install in development mode for local testing:
```bash
cd Logpy_v2
pip install -e .
```

### Option 3: Direct Import
Clone the repository and add it to your Python path in your project.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/PatrickEasy/Logpy_v2.git
cd Logpy_v2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install -r requirements-dev.txt  # Optional
```

### Running Tests

```bash
pytest tests/
```

## Project Structure

```
Logpy_v2/
├── README.md
├── requirements.txt
├── setup.py
├── logpy_v2/
│   ├── __init__.py
│   ├── logger.py
│   └── formatters.py
├── tests/
│   └── test_logger.py
└── examples/
    └── basic_usage.py
```

## Contributing

This is a personal project, but suggestions and improvements are welcome. Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this in your personal projects.

## Roadmap

- [ ] Add JSON logging format support
- [ ] Implement log filtering capabilities
- [ ] Add context managers for scoped logging
- [ ] Create decorators for function logging
- [ ] Add async logging support
- [ ] Implement log aggregation features

## Changelog

### Version 2.0.0 (In Development)
- Initial setup of Logpy_v2
- Project structure created
- Basic documentation added

## Author

Patrick Easy

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/PatrickEasy/Logpy_v2/issues).
