# Super_red_team_bot

![CI](https://github.com/houston2394/Super_red_team_bot/actions/workflows/ci.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An extensible automation toolkit for red team operations, penetration testing, and security reconnaissance. Features a plugin-based architecture, concurrent endpoint scanning, parameter fuzzing, and a CLI interface for orchestrating security assessments.

## Features

- **Plugin System** — Dynamic plugin loader that discovers, loads, and executes plugins from the `plugins/` directory
- **Endpoint Scanner** — Concurrent scanning of 48+ common paths using ThreadPoolExecutor
- **Parameter Fuzzer** — Tests 40+ common parameters with 17 payload types and baseline response diffing
- **CLI Interface** — Full argparse CLI with plugin selection, target specification, and output options
- **OpenCode Agents** — 5 TypeScript agents (vuln-classifier, secure-reviewer, threat-modeler, recon-analyzer, exploit-sketcher) with input validation and error handling
- **Security Hooks** — Recursive secret scrubbing and network guard with blocked domain enforcement

## Installation

```bash
# Clone the repository
git clone https://github.com/houston2394/Super_red_team_bot.git
cd Super_red_team_bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

## Usage

### List available plugins

```bash
python3 bot.py --list-plugins
```

### Run a specific plugin against a target

```bash
python3 bot.py --plugin example_plugin --target https://example.com
```

### Full options

```bash
python3 bot.py --target https://example.com --output results.json --verbose
```

### CLI Arguments

| Argument | Description |
|----------|-------------|
| `--list-plugins` | List all discovered plugins and exit |
| `--plugin NAME` | Run a specific plugin by name |
| `--target URL` | Target URL for scanning/fuzzing |
| `--output FILE` | Output file for results (JSON) |
| `--verbose` | Enable verbose logging |

## Plugin Development

Create new plugins by adding a `.py` file to the `plugins/` directory:

```python
PLUGIN_INFO = {
    "name": "my_plugin",
    "description": "What this plugin does",
    "version": "0.1.0",
    "author": "Your Name"
}

def run(**kwargs):
    """Plugin entry point. Receives target, config, and other kwargs."""
    target = kwargs.get("target", "")
    return {"status": "complete", "results": []}
```

See `plugins/example_plugin.py` for a complete reference implementation.

## Project Structure

```
Super_red_team_bot/
├── bot.py                  # Main entry point (CLI + RedTeamBot class)
├── requirements.txt        # Python dependencies
├── Makefile                # install, test, clean, run, lint targets
├── .env.example            # Environment configuration template
├── config/
│   └── sample_config.ini   # Bot configuration template
├── plugins/
│   ├── __init__.py         # Package init
│   ├── loader.py           # PluginLoader (discover, load, execute)
│   └── example_plugin.py   # Reference plugin implementation
├── recon/
│   ├── __init__.py         # Package init
│   ├── scanner.py          # EndpointScanner (concurrent, 48+ paths)
│   ├── fuzzer.py           # ParameterFuzzer (baseline diffing)
│   ├── endpoints.json      # Endpoint data
│   └── params.json         # Parameter data
├── tests/
│   ├── test_bot.py         # Bot unit tests
│   ├── test_plugin_loader.py  # Plugin loader tests
│   ├── test_scanner.py     # Scanner tests
│   ├── test_fuzzer.py      # Fuzzer tests
│   ├── test_requirements.py   # Infrastructure tests
│   └── agent-eval/         # Agent evaluation scenarios
└── .opencode/
    ├── agents/             # 5 TypeScript agents
    └── hooks/              # 3 security hooks
```

## Testing

```bash
# Run all tests
make test

# Or directly
python3 -m pytest tests/ -v

# Run specific test
python3 -m pytest tests/test_scanner.py -v
```

## Configuration

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `TARGET_BASE_URL` | `https://example.com` | Default target URL |
| `MAX_THREADS` | `5` | Concurrent scanner threads |
| `REQUEST_TIMEOUT` | `30` | HTTP request timeout (seconds) |
| `PLUGINS_ENABLED` | `example_plugin` | Comma-separated plugin list |
| `OUTPUT_DIR` | `./recon` | Output directory for results |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing, plugin development, and responsible disclosure.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for **authorized security testing and educational purposes only**. Users are responsible for ensuring they have proper authorization before testing any systems. Unauthorized access to computer systems is illegal. The authors assume no liability for misuse of this software.
