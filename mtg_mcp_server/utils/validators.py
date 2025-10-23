"""Validation utilities for MTG API client parameters."""

from mtg_mcp_server.models.exceptions import MTGValidationError


def validate_card_name(name: str) -> None:
    """Validate card name parameter.

    Args:
        name: Card name to validate

    Raises:
        MTGValidationError: If name is empty or whitespace-only
    """
    if not name.strip():
        raise MTGValidationError("Card name cannot be empty")


def validate_card_id(card_id: str) -> None:
    """Validate card ID parameter.

    Args:
        card_id: Card ID to validate

    Raises:
        MTGValidationError: If card_id is empty or whitespace-only
    """
    if not card_id.strip():
        raise MTGValidationError("Card ID cannot be empty")


def validate_search_limit(limit: int) -> None:
    """Validate search limit parameter.

    Args:
        limit: Search limit to validate

    Raises:
        MTGValidationError: If limit is not between 1 and 50
    """
    if not (1 <= limit <= 50):
        raise MTGValidationError("Limit must be between 1 and 50")


def validate_filter_limit(limit: int) -> None:
    """Validate filter limit parameter.

    Args:
        limit: Filter limit to validate

    Raises:
        MTGValidationError: If limit is not between 1 and 100
    """
    if not (1 <= limit <= 100):
        raise MTGValidationError("Limit must be between 1 and 100")


def validate_random_count(count: int) -> None:
    """Validate random count parameter.

    Args:
        count: Random count to validate

    Raises:
        MTGValidationError: If count is not between 1 and 10
    """
    if not (1 <= count <= 10):
        raise MTGValidationError("Count must be between 1 and 10")
