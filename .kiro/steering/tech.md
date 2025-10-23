# Technology Stack

## Build System & Package Management

- **Build System**: setuptools with pyproject.toml configuration
- **Python Version**: Requires Python 3.8+
- **Package Manager**: pip (standard Python package installer)

## Core Dependencies

- **mcp**: Model Context Protocol library (>=1.0.0)
- **httpx**: Async HTTP client for API requests (>=0.25.0)
- **pydantic**: Data validation and serialization (>=2.0.0)
- **asyncio-throttle**: Rate limiting for API calls (>=1.0.0)

## Development Tools

- **Testing**: pytest with asyncio support
- **Code Formatting**: black (line length: 88)
- **Import Sorting**: isort (black-compatible profile)
- **Type Checking**: mypy with strict typing
- **Linting**: flake8

## Common Commands

### Development Setup

```bash
# Create virtual environment
python -m venv mtg-mcp-env

# Activate (Windows)
mtg-mcp-env\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format code
black mtg_mcp_server tests
isort mtg_mcp_server tests

# Type checking
mypy mtg_mcp_server

# Run tests
pytest
```

### Running the Server

```bash
# Direct execution
python -m mtg_mcp_server.main

# Or via entry point
mtg-mcp-server
```

## Architecture Pattern

- **Async/Await**: All API operations use async patterns
- **MCP Protocol**: Standard Model Context Protocol implementation
- **Modular Design**: Separated concerns (API client, models, tools, handlers)
- **Error Handling**: Centralized exception handling with user-friendly messages
