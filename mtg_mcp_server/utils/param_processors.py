"""Parameter processing utilities for MTG API requests."""

from typing import Dict, Any, List


def build_search_params(name: str, limit: int = 10) -> Dict[str, Any]:
    """Build parameters for card search requests.

    Args:
        name: Card name to search for
        limit: Maximum number of results

    Returns:
        Dictionary of API parameters
    """
    return {"name": name, "pageSize": limit}


def build_filter_params(filters: Dict[str, Any], limit: int = 20) -> Dict[str, Any]:
    """Build parameters for card filter requests.

    Args:
        filters: Filter criteria
        limit: Maximum number of results

    Returns:
        Dictionary of API parameters
    """
    params = {"pageSize": limit}

    for key, value in filters.items():
        if key == "colors" and isinstance(value, list):
            params["colors"] = ",".join(value)
        else:
            params[key] = value

    return params


def build_random_params(count: int = 1) -> Dict[str, Any]:
    """Build parameters for random card requests.

    Args:
        count: Number of random cards to retrieve

    Returns:
        Dictionary of API parameters
    """
    return {"random": "true", "pageSize": count}
