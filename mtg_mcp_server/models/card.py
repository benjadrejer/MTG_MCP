"""Card data model for MTG MCP Server."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Card:
    """MTG Card data model with all API attributes."""

    id: str
    name: str
    mana_cost: Optional[str] = None
    cmc: Optional[int] = None
    colors: List[str] = field(default_factory=list)
    color_identity: List[str] = field(default_factory=list)
    type: Optional[str] = None
    supertypes: List[str] = field(default_factory=list)
    types: List[str] = field(default_factory=list)
    subtypes: List[str] = field(default_factory=list)
    text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None
    loyalty: Optional[str] = None
    set_name: Optional[str] = None
    set_code: Optional[str] = None
    rarity: Optional[str] = None
    image_url: Optional[str] = None
