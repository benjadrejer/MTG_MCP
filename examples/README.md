# MTG MCP Server Examples

This directory contains examples and test scripts for the MTG MCP Server.

## Current Functionality

The MTG MCP Server currently implements the following tools:

### `search_cards`

Search for Magic the Gathering cards by name with partial matching support.

**Parameters:**

- `name` (required): Card name or partial name to search for
- `limit` (optional): Maximum number of results to return (default: 10, max: 50)

**Example usage:**

```json
{
  "name": "search_cards",
  "arguments": {
    "name": "Lightning Bolt",
    "limit": 5
  }
}
```

## Configuration

### MCP Client Configuration

Add the following to your MCP client configuration file (e.g., `mcp.json`):

```json
{
  "mcpServers": {
    "mtg-mcp-server": {
      "command": "mtg-mcp-server",
      "args": [],
      "env": {
        "PYTHONPATH": ".",
        "LOG_LEVEL": "INFO"
      },
      "disabled": false,
      "autoApprove": ["search_cards"]
    }
  }
}
```

### Environment Variables

- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `PYTHONPATH`: Ensure the server can find the mtg_mcp_server module

## Testing

### Manual Testing

Run the server directly:

```bash
python -m mtg_mcp_server.main
```

### Automated Testing

Run the test script:

```bash
python examples/test_mcp_server.py
```

This will:

1. Start the MCP server
2. Test the search_cards tool with various inputs
3. Validate error handling
4. Report results

## Example Queries

### Basic Card Search

```json
{ "name": "Lightning Bolt" }
```

### Limited Results

```json
{ "name": "Lightning", "limit": 3 }
```

### Partial Name Matching

```json
{ "name": "Jace" }
```

## Expected Output Format

The search_cards tool returns formatted text with:

- Card name (bolded)
- Mana cost
- Card type
- Power/Toughness (for creatures)
- Loyalty (for planeswalkers)
- Card text
- Set information
- Rarity

Example output:

```
Found 1 cards matching 'Lightning Bolt':

1. **Lightning Bolt**
   Mana Cost: {R}
   Type: Instant
   Text: Lightning Bolt deals 3 damage to any target.
   Set: Limited Edition Alpha (LEA)
   Rarity: Common
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH includes the project root
2. **API Timeouts**: The MTG API may be slow; increase timeout if needed
3. **Rate Limiting**: The server implements rate limiting (10 requests/second)

### Debug Mode

Set `LOG_LEVEL=DEBUG` to see detailed request/response information.
