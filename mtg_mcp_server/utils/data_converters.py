"""Data conversion utilities for MTG API responses."""

from typing import Dict, Any

from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.set import Set


def convert_card_data(api_data: Dict[str, Any]) -> Card:
    """Convert API response data to Card object.

    Args:
        api_data: Raw card data from MTG API

    Returns:
        Card object with converted data
    """
    return Card(
        id=api_data.get("id", ""),
        name=api_data.get("name", ""),
        mana_cost=api_data.get("manaCost"),
        cmc=api_data.get("cmc"),
        colors=api_data.get("colors", []),
        color_identity=api_data.get("colorIdentity", []),
        type=api_data.get("type"),
        supertypes=api_data.get("supertypes", []),
        types=api_data.get("types", []),
        subtypes=api_data.get("subtypes", []),
        text=api_data.get("text"),
        power=api_data.get("power"),
        toughness=api_data.get("toughness"),
        loyalty=api_data.get("loyalty"),
        set_name=api_data.get("setName"),
        set_code=api_data.get("set"),
        rarity=api_data.get("rarity"),
        image_url=api_data.get("imageUrl"),
    )


def convert_set_data(api_data: Dict[str, Any]) -> Set:
    """Convert API response data to Set object.

    Args:
        api_data: Raw set data from MTG API

    Returns:
        Set object with converted data
    """
    return Set(
        code=api_data.get("code", ""),
        name=api_data.get("name", ""),
        type=api_data.get("type"),
        release_date=api_data.get("releaseDate"),
        block=api_data.get("block"),
        online_only=api_data.get("onlineOnly", False),
        card_count=api_data.get("cardCount"),
    )
