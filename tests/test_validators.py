"""Unit tests for validation utilities."""

import pytest
from mtg_mcp_server.models.exceptions import MTGValidationError
from mtg_mcp_server.utils.validators import (
    validate_card_name,
    validate_card_id,
    validate_search_limit,
    validate_filter_limit,
    validate_random_count,
)


class TestValidators:
    """Test cases for validation utilities."""

    def test_validate_card_name_valid(self):
        """Test valid card name validation."""
        # Should not raise any exception
        validate_card_name("Lightning Bolt")
        validate_card_name("Black Lotus")
        validate_card_name("Jace, the Mind Sculptor")

    def test_validate_card_name_empty_string(self):
        """Test empty string card name validation."""
        with pytest.raises(MTGValidationError, match="Card name cannot be empty"):
            validate_card_name("")

    def test_validate_card_name_whitespace_only(self):
        """Test whitespace-only card name validation."""
        with pytest.raises(MTGValidationError, match="Card name cannot be empty"):
            validate_card_name("   ")

        with pytest.raises(MTGValidationError, match="Card name cannot be empty"):
            validate_card_name("\t\n")

    def test_validate_card_id_valid(self):
        """Test valid card ID validation."""
        # Should not raise any exception
        validate_card_id("12345")
        validate_card_id("abc-123")
        validate_card_id("card_id_123")

    def test_validate_card_id_empty_string(self):
        """Test empty string card ID validation."""
        with pytest.raises(MTGValidationError, match="Card ID cannot be empty"):
            validate_card_id("")

    def test_validate_card_id_whitespace_only(self):
        """Test whitespace-only card ID validation."""
        with pytest.raises(MTGValidationError, match="Card ID cannot be empty"):
            validate_card_id("   ")

    def test_validate_search_limit_valid(self):
        """Test valid search limit validation."""
        # Should not raise any exception
        validate_search_limit(1)
        validate_search_limit(25)
        validate_search_limit(50)

    def test_validate_search_limit_too_low(self):
        """Test search limit too low."""
        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 50"):
            validate_search_limit(0)

        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 50"):
            validate_search_limit(-1)

    def test_validate_search_limit_too_high(self):
        """Test search limit too high."""
        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 50"):
            validate_search_limit(51)

        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 50"):
            validate_search_limit(100)

    def test_validate_filter_limit_valid(self):
        """Test valid filter limit validation."""
        # Should not raise any exception
        validate_filter_limit(1)
        validate_filter_limit(50)
        validate_filter_limit(100)

    def test_validate_filter_limit_too_low(self):
        """Test filter limit too low."""
        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 100"):
            validate_filter_limit(0)

    def test_validate_filter_limit_too_high(self):
        """Test filter limit too high."""
        with pytest.raises(MTGValidationError, match="Limit must be between 1 and 100"):
            validate_filter_limit(101)

    def test_validate_random_count_valid(self):
        """Test valid random count validation."""
        # Should not raise any exception
        validate_random_count(1)
        validate_random_count(5)
        validate_random_count(10)

    def test_validate_random_count_too_low(self):
        """Test random count too low."""
        with pytest.raises(MTGValidationError, match="Count must be between 1 and 10"):
            validate_random_count(0)

    def test_validate_random_count_too_high(self):
        """Test random count too high."""
        with pytest.raises(MTGValidationError, match="Count must be between 1 and 10"):
            validate_random_count(11)
