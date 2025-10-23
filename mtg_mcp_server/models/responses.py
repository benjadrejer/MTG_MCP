"""API response wrapper classes for MTG MCP Server."""

from dataclasses import dataclass, field
from typing import List, Optional

from .card import Card
from .set import Set


@dataclass
class APIResponse:
    """Wrapper for MTG API responses."""

    cards: List[Card] = field(default_factory=list)
    sets: List[Set] = field(default_factory=list)


@dataclass
class ErrorResponse:
    """Error response wrapper for API failures."""

    error: str
    status_code: int
    details: Optional[str] = None
