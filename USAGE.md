# MTG MCP Server Usage Guide

The MTG MCP Server is now ready for testing with the `search_cards` tool implemented.

## Quick Start

### 1. Install the Server

```bash
# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### 2. Test the Server

```bash
# Validate server setup
python examples/validate_server.py

# Run integration tests
python examples/test_integration.py
```

### 3. Install as MCP Server

The server needs to be installed so the `mtg-mcp-server` command is available:

```bash
# Make sure you're in the project directory
cd /path/to/mtg-mcp-server

# Install the package (creates the mtg-mcp-server command)
pip install -e .
```

### 4. Verify Installation

```bash
# Test that the command is available
where mtg-mcp-server    # Windows
which mtg-mcp-server    # Linux/Mac
# Should show: /path/to/your/venv/Scripts/mtg-mcp-server.exe (Windows)
# Should show: /path/to/your/venv/bin/mtg-mcp-server (Linux/Mac)

# Test that the server starts correctly
mtg-mcp-server
# Should show:
# INFO - Starting MTG MCP Server...
# INFO - MTG MCP Server initialized successfully
# (Then press Ctrl+C to stop)
```

### 5. Configure MCP Client

Add to your MCP client configuration (e.g., `~/.kiro/settings/mcp.json`):

**Option A: Using the installed command (recommended)**

```json
{
  "mcpServers": {
    "mtg-mcp-server": {
      "command": "mtg-mcp-server",
      "args": [],
      "disabled": false,
      "autoApprove": ["search_cards"]
    }
  }
}
```

**Option B: Using Python module directly**

```json
{
  "mcpServers": {
    "mtg-mcp-server": {
      "command": "python",
      "args": ["-m", "mtg_mcp_server.main"],
      "env": {
        "PYTHONPATH": "/path/to/mtg-mcp-server"
      },
      "disabled": false,
      "autoApprove": ["search_cards"]
    }
  }
}
```

**Option C: Using full path to Python executable**

```json
{
  "mcpServers": {
    "mtg-mcp-server": {
      "command": "/path/to/your/venv/Scripts/python.exe",
      "args": ["-m", "mtg_mcp_server.main"],
      "cwd": "/path/to/mtg-mcp-server",
      "disabled": false,
      "autoApprove": ["search_cards"]
    }
  }
}
```

## Available Tools

### `search_cards`

Search for Magic the Gathering cards by name.

**Parameters:**

- `name` (string, required): Card name or partial name
- `limit` (integer, optional): Max results (default: 10, max: 50)

**Example:**

```json
{
  "name": "search_cards",
  "arguments": {
    "name": "Lightning Bolt",
    "limit": 5
  }
}
```

**Output:**

```
Found 1 cards matching 'Lightning Bolt':

1. **Lightning Bolt**
   Mana Cost: {R}
   Type: Instant
   Text: Lightning Bolt deals 3 damage to any target.
   Set: Limited Edition Alpha (LEA)
   Rarity: Common
```

## Features Implemented

✅ **Card Search**: Name-based search with partial matching  
✅ **Result Limiting**: Configurable result limits  
✅ **Rich Formatting**: Detailed card information display  
✅ **Error Handling**: Graceful error messages  
✅ **MCP Compliance**: Full MCP protocol support  
✅ **Rate Limiting**: Built-in API rate limiting  
✅ **Async Support**: Non-blocking operations

## Testing

The server has been validated with:

- 68 unit tests (all passing)
- Integration tests for MCP protocol
- End-to-end functionality tests
- Error handling validation

## Next Steps

The following tools will be implemented in future tasks:

- `filter_cards`: Filter cards by attributes (color, type, etc.)
- `get_card_details`: Get detailed information for specific cards
- `get_sets`: Retrieve MTG set information
- `get_random_cards`: Get random cards for discovery

## Troubleshooting

### Common Issues

1. **"Command not found" Error**:

   - Make sure you've installed the package: `pip install -e .`
   - Verify the command exists: `which mtg-mcp-server` or `where mtg-mcp-server`
   - Try using Option B or C from the configuration above

2. **MCP Client Connection Fails**:

   - Check that the command path is correct in your mcp.json
   - Ensure you're using the right Python environment
   - Try running the server manually first: `mtg-mcp-server` (should start and wait for input)
   - Use full paths if relative paths don't work

3. **Import Errors**:

   - Ensure the package is installed with `pip install -e .`
   - Check that all dependencies are installed: `pip install -e ".[dev]"`
   - Verify PYTHONPATH includes the project directory

4. **API Timeouts**:

   - The MTG API may be slow during peak times
   - Check your internet connection
   - Try with a smaller limit parameter

5. **Permission Issues**:
   - On Windows, make sure the Scripts directory is in your PATH
   - Try running your terminal/IDE as administrator if needed

### Manual Testing

You can test the server manually before adding it to your MCP client:

```bash
# Run the server directly (it will wait for MCP protocol input)
mtg-mcp-server

# Or with debug logging
LOG_LEVEL=DEBUG mtg-mcp-server

# Or using Python module
python -m mtg_mcp_server.main
```

The server should start and display:

```
INFO - Starting MTG MCP Server...
INFO - MTG MCP Server initialized successfully
```

Then it will wait for MCP protocol messages. Press Ctrl+C to stop.

### Debug Mode

Set environment variable `LOG_LEVEL=DEBUG` for detailed logging:

```bash
LOG_LEVEL=DEBUG mtg-mcp-server
```

### Verify MCP Protocol

You can test the MCP protocol manually by sending JSON messages to the server:

1. Start the server: `mtg-mcp-server`
2. Send initialization message (copy and paste, then press Enter):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": { "name": "test-client", "version": "1.0.0" }
  }
}
```

3. The server should respond with its capabilities including the search_cards tool.
