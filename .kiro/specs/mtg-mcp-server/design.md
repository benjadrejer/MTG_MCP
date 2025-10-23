# MTG MCP Server Design Document

## Overview

The MTG MCP Server is a Model Context Protocol server that provides AI assistants with tools to interact with the Magic the Gathering API. The server exposes a set of standardized tools that allow querying card information, searching by various criteria, retrieving set data, and discovering random cards.

The server will be implemented as a Python-based MCP server using the `mcp` library, providing a clean interface between AI assistants and the MTG API at https://api.magicthegathering.io.

## Architecture

### High-Level Architecture

```
AI Assistant (Kiro/Claude)
    ↓ MCP Protocol
MCP Server (Python)
    ↓ HTTP Requests
MTG API (api.magicthegathering.io)
```

### Component Structure

- **MCP Server Core**: Handles MCP protocol communication and tool registration
- **MTG API Client**: Manages HTTP requests to the MTG API with error handling
- **Tool Handlers**: Individual functions that implement each MCP tool
- **Data Models**: Type definitions for MTG cards, sets, and API responses
- **Error Handler**: Centralized error handling and logging

## Components and Interfaces

### MCP Tools

The server will expose the following MCP tools:

#### 1. `search_cards`

- **Purpose**: Search for MTG cards by name with partial matching
- **Parameters**:
  - `name` (required): Card name or partial name to search for
  - `limit` (optional): Maximum number of results (default: 10, max: 50)
- **Returns**: Array of card objects with basic information

#### 2. `get_card_details`

- **Purpose**: Get detailed information for a specific card
- **Parameters**:
  - `card_id` (required): MTG API card ID
- **Returns**: Complete card object with all available attributes

#### 3. `filter_cards`

- **Purpose**: Filter cards by various attributes
- **Parameters**:
  - `colors` (optional): Array of color identifiers (W, U, B, R, G)
  - `type` (optional): Card type (creature, instant, sorcery, etc.)
  - `cmc` (optional): Converted mana cost
  - `set` (optional): Set code
  - `limit` (optional): Maximum results (default: 20, max: 100)
- **Returns**: Array of matching cards

#### 4. `get_sets`

- **Purpose**: Retrieve information about MTG sets
- **Parameters**:
  - `set_code` (optional): Specific set code to retrieve
  - `name` (optional): Set name to search for
- **Returns**: Array of set objects or single set if code specified

#### 5. `get_random_cards`

- **Purpose**: Get random MTG cards for discovery
- **Parameters**:
  - `count` (optional): Number of random cards (default: 1, max: 10)
- **Returns**: Array of random card objects

### MTG API Client

```python
class MTGAPIClient:
    def __init__(self, base_url: str = "https://api.magicthegathering.io/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "MTG-MCP-Server/1.0"})

    async def search_cards(self, name: str, limit: int = 10) -> List[Card]
    async def get_card(self, card_id: str) -> Card
    async def filter_cards(self, **filters) -> List[Card]
    async def get_sets(self, set_code: str = None) -> List[Set]
    async def get_random_cards(self, count: int = 1) -> List[Card]
```

## Data Models

### Card Model

```python
@dataclass
class Card:
    id: str
    name: str
    mana_cost: Optional[str]
    cmc: Optional[int]
    colors: List[str]
    color_identity: List[str]
    type: str
    supertypes: List[str]
    types: List[str]
    subtypes: List[str]
    text: Optional[str]
    power: Optional[str]
    toughness: Optional[str]
    loyalty: Optional[str]
    set_name: Optional[str]
    set_code: Optional[str]
    rarity: Optional[str]
    image_url: Optional[str]
```

### Set Model

```python
@dataclass
class Set:
    code: str
    name: str
    type: str
    release_date: Optional[str]
    block: Optional[str]
    online_only: bool
    card_count: Optional[int]
```

### API Response Models

```python
@dataclass
class APIResponse:
    cards: List[Card] = field(default_factory=list)
    sets: List[Set] = field(default_factory=list)

@dataclass
class ErrorResponse:
    error: str
    status_code: int
    details: Optional[str] = None
```

## Error Handling

### Error Categories

1. **API Errors**: HTTP errors from MTG API (4xx, 5xx responses)
2. **Network Errors**: Connection timeouts, DNS failures
3. **Validation Errors**: Invalid parameters passed to tools
4. **Rate Limiting**: API rate limit exceeded

### Error Handling Strategy

- **Graceful Degradation**: Return meaningful error messages to users
- **Retry Logic**: Implement exponential backoff for transient failures
- **Timeout Handling**: 30-second timeout for API requests
- **Logging**: Log all errors with context for debugging
- **User-Friendly Messages**: Convert technical errors to readable messages

```python
class MTGAPIError(Exception):
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def handle_api_error(response: httpx.Response) -> None:
    if response.status_code == 404:
        raise MTGAPIError("Resource not found", 404)
    elif response.status_code == 429:
        raise MTGAPIError("Rate limit exceeded, please try again later", 429)
    elif response.status_code >= 500:
        raise MTGAPIError("MTG API service unavailable", response.status_code)
    else:
        raise MTGAPIError(f"API request failed: {response.status_code}", response.status_code)
```

## Testing Strategy

### Unit Testing

- Test each MCP tool handler independently
- Mock MTG API responses for consistent testing
- Validate data model serialization/deserialization
- Test error handling scenarios

### Integration Testing

- Test actual MTG API integration with rate limiting
- Validate MCP protocol compliance
- Test end-to-end tool execution flows

### Test Data

- Use known MTG cards for consistent test results
- Create mock API responses for edge cases
- Test with various card types and attributes

### Testing Tools

- `pytest` for test framework
- `pytest-asyncio` for async test support
- `httpx-mock` for API mocking
- `mcp-test-client` for MCP protocol testing

## Implementation Considerations

### Performance

- Implement response caching for frequently requested cards
- Use connection pooling for HTTP requests
- Limit concurrent API requests to respect rate limits

### Security

- Validate all input parameters to prevent injection attacks
- Implement request size limits
- Use HTTPS for all API communications

### Maintainability

- Follow Python typing best practices
- Implement comprehensive logging
- Use configuration files for API endpoints and limits
- Document all public interfaces

### Deployment

- Package as a standalone Python application
- Support installation via pip
- Provide Docker container option
- Include example MCP configuration
