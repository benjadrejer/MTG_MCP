"""Unit tests for parameter processing utilities."""

import pytest
from mtg_mcp_server.utils.param_processors import (
    build_search_params,
    build_filter_params,
    build_random_params,
)


class TestParamProcessors:
    """Test cases for parameter processing utilities."""

    def test_build_search_params_basic(self):
        """Test basic search parameters building."""
        params = build_search_params("Lightning Bolt", 10)

        expected = {"name": "Lightning Bolt", "pageSize": 10}
        assert params == expected

    def test_build_search_params_default_limit(self):
        """Test search parameters with default limit."""
        params = build_search_params("Lightning Bolt")

        expected = {"name": "Lightning Bolt", "pageSize": 10}
        assert params == expected

    def test_build_filter_params_single_filter(self):
        """Test filter parameters with single filter."""
        filters = {"type": "Instant"}
        params = build_filter_params(filters, 20)

        expected = {"pageSize": 20, "type": "Instant"}
        assert params == expected

    def test_build_filter_params_multiple_filters(self):
        """Test filter parameters with multiple filters."""
        filters = {"type": "Creature", "cmc": 3, "rarity": "Rare"}
        params = build_filter_params(filters, 25)

        expected = {"pageSize": 25, "type": "Creature", "cmc": 3, "rarity": "Rare"}
        assert params == expected

    def test_build_filter_params_colors_list(self):
        """Test filter parameters with colors as list."""
        filters = {"colors": ["Red", "Blue"], "type": "Instant"}
        params = build_filter_params(filters, 15)

        expected = {"pageSize": 15, "colors": "Red,Blue", "type": "Instant"}
        assert params == expected

    def test_build_filter_params_colors_single_item_list(self):
        """Test filter parameters with single color in list."""
        filters = {"colors": ["Green"]}
        params = build_filter_params(filters, 10)

        expected = {"pageSize": 10, "colors": "Green"}
        assert params == expected

    def test_build_filter_params_colors_empty_list(self):
        """Test filter parameters with empty colors list."""
        filters = {"colors": []}
        params = build_filter_params(filters, 10)

        expected = {"pageSize": 10, "colors": ""}
        assert params == expected

    def test_build_filter_params_no_filters(self):
        """Test filter parameters with no filters."""
        filters = {}
        params = build_filter_params(filters, 30)

        expected = {"pageSize": 30}
        assert params == expected

    def test_build_filter_params_default_limit(self):
        """Test filter parameters with default limit."""
        filters = {"type": "Sorcery"}
        params = build_filter_params(filters)

        expected = {"pageSize": 20, "type": "Sorcery"}
        assert params == expected

    def test_build_random_params_basic(self):
        """Test basic random parameters building."""
        params = build_random_params(5)

        expected = {"random": "true", "pageSize": 5}
        assert params == expected

    def test_build_random_params_default_count(self):
        """Test random parameters with default count."""
        params = build_random_params()

        expected = {"random": "true", "pageSize": 1}
        assert params == expected

    def test_build_random_params_single_card(self):
        """Test random parameters for single card."""
        params = build_random_params(1)

        expected = {"random": "true", "pageSize": 1}
        assert params == expected
