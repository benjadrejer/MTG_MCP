"""Set data model for MTG MCP Server."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Set:
    """MTG Set data model with all API attributes."""

    code: str
    name: str
    type: Optional[str] = None
    release_date: Optional[str] = None
    block: Optional[str] = None
    online_only: bool = False
    card_count: Optional[int] = None
