# Contributing to Super_red_team_bot

Thank you for your interest in contributing! This project is a security tool, so contributions require extra care around responsible use and disclosure.

## Security Vulnerabilities

**Do NOT open a public issue for security vulnerabilities.**

If you discover a security vulnerability in this tool, please report it responsibly:

1. Email the maintainer directly (see profile for contact)
2. Include a detailed description of the vulnerability
3. Allow reasonable time for a fix before public disclosure

## Development Setup

```bash
# Clone the repository
git clone https://github.com/houston2394/Super_red_team_bot.git
cd Super_red_team_bot

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Run tests to verify setup
make test
```

## Running Tests

```bash
# Run all tests
make test

# Or directly with pytest
python3 -m pytest tests/ -v

# Run a specific test file
python3 -m pytest tests/test_scanner.py -v
```

## Making Changes

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass (`make test`)
4. Write tests for new functionality
5. Submit a pull request against `main`

### PR Requirements

- All existing tests must pass
- New features must include tests
- Follow existing code style and patterns
- Update documentation if applicable

### Code Style

- Python: Follow PEP 8
- Use descriptive variable and function names
- Add docstrings to public classes and methods
- Keep functions focused and small

## Writing Plugins

The plugin system is designed for extensibility. To create a new plugin:

1. Create a new `.py` file in the `plugins/` directory
2. Define a `PLUGIN_INFO` dictionary with metadata
3. Implement a `run()` function as the entry point

See `plugins/example_plugin.py` for a complete reference implementation.

```python
PLUGIN_INFO = {
    "name": "my_plugin",
    "description": "What this plugin does",
    "version": "0.1.0",
    "author": "Your Name"
}

def run(**kwargs):
    """Plugin entry point."""
    target = kwargs.get("target", "")
    # Your implementation here
    return {"status": "complete", "results": []}
```

## Ethical Use

This tool is intended for **authorized security testing only**. Contributors must:

- Only test systems you have explicit permission to test
- Follow all applicable laws and regulations
- Never use this tool for malicious purposes
- Include appropriate warnings in any new offensive capabilities

## Questions?

Open an issue for questions about contributing, feature requests, or bug reports (non-security).
