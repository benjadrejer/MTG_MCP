# Project Structure

## Root Directory Layout

```
mtg-mcp-server/
├── .kiro/                    # Kiro IDE configuration and specs
├── .vscode/                  # VS Code settings
├── mtg_mcp_server/          # Main package directory
├── mtg_mcp_server.egg-info/ # Package metadata (generated)
├── tests/                   # Test files
├── pyproject.toml          # Project configuration and dependencies
└── README.md               # Project documentation
```

## Main Package Structure

```
mtg_mcp_server/
├── __init__.py             # Package initialization
├── main.py                 # Entry point and server setup
├── api/                    # MTG API client layer
│   ├── __init__.py
│   └── client.py          # HTTP client for MTG API
├── models/                 # Data models and type definitions
│   ├── __init__.py
│   ├── card.py            # Card data model
│   ├── set.py             # Set data model
│   ├── responses.py       # API response models
│   └── exceptions.py      # Custom exception classes
├── utils/                  # Utility functions and helpers
│   ├── __init__.py
│   ├── data_converters.py # API response to model conversion
│   ├── validators.py      # Input parameter validation
│   └── param_processors.py # API parameter building
└── tools/                  # MCP tool implementations
    ├── __init__.py
    └── handlers.py        # Tool handler functions
```

## Organizational Principles

### Separation of Concerns

- **api/**: External API communication and HTTP handling
- **models/**: Data structures, validation, and type safety
- **utils/**: Utility functions for data conversion, validation, and parameter processing
- **tools/**: MCP protocol tool implementations
- **main.py**: Application entry point and server orchestration

### Naming Conventions

- **Files**: snake_case for all Python files
- **Classes**: PascalCase (e.g., `MTGAPIClient`, `Card`)
- **Functions/Variables**: snake_case (e.g., `search_cards`, `api_client`)
- **Constants**: UPPER_SNAKE_CASE

### Import Organization

- Standard library imports first
- Third-party imports second
- Local package imports last
- Use absolute imports within the package

### File Responsibilities

- **main.py**: Server initialization, MCP setup, CLI entry point
- **api/client.py**: All MTG API HTTP requests and response handling
- **models/**: Pydantic models for data validation and serialization
- **utils/data_converters.py**: Convert API responses to data models
- **utils/validators.py**: Validate input parameters and raise appropriate errors
- **utils/param_processors.py**: Build API request parameters from inputs
- **tools/handlers.py**: MCP tool registration and implementation
- **tests/**: Mirror the main package structure for test organization
