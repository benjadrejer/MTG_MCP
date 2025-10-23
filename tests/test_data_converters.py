"""Unit tests for data conversion utilities."""

import pytest
from mtg_mcp_server.models.card import Card
from mtg_mcp_server.models.set import Set
from mtg_mcp_server.utils.data_converters import convert_card_data, convert_set_data


class TestDataConverters:
    """Test cases for data conversion utilities."""

    def test_convert_card_data_complete(self):
        """Test card data conversion with all fields."""
        api_data = {
            "id": "1",
            "name": "Lightning Bolt",
            "manaCost": "{R}",
            "cmc": 1,
            "colors": ["Red"],
            "colorIdentity": ["R"],
            "type": "Instant",
            "supertypes": [],
            "types": ["Instant"],
            "subtypes": [],
            "text": "Lightning Bolt deals 3 damage to any target.",
            "power": None,
            "toughness": None,
            "loyalty": None,
            "set": "LEA",
            "setName": "Limited Edition Alpha",
            "rarity": "Common",
            "imageUrl": "http://example.com/image.jpg",
        }

        card = convert_card_data(api_data)

        assert isinstance(card, Card)
        assert card.id == "1"
        assert card.name == "Lightning Bolt"
        assert card.mana_cost == "{R}"
        assert card.cmc == 1
        assert card.colors == ["Red"]
        assert card.color_identity == ["R"]
        assert card.type == "Instant"
        assert card.supertypes == []
        assert card.types == ["Instant"]
        assert card.subtypes == []
        assert card.text == "Lightning Bolt deals 3 damage to any target."
        assert card.power is None
        assert card.toughness is None
        assert card.loyalty is None
        assert card.set_code == "LEA"
        assert card.set_name == "Limited Edition Alpha"
        assert card.rarity == "Common"
        assert card.image_url == "http://example.com/image.jpg"

    def test_convert_card_data_minimal(self):
        """Test card data conversion with minimal fields."""
        api_data = {"id": "2", "name": "Test Card"}

        card = convert_card_data(api_data)

        assert isinstance(card, Card)
        assert card.id == "2"
        assert card.name == "Test Card"
        assert card.mana_cost is None
        assert card.cmc is None
        assert card.colors == []
        assert card.color_identity == []
        assert card.type is None
        assert card.supertypes == []
        assert card.types == []
        assert card.subtypes == []
        assert card.text is None
        assert card.power is None
        assert card.toughness is None
        assert card.loyalty is None
        assert card.set_code is None
        assert card.set_name is None
        assert card.rarity is None
        assert card.image_url is None

    def test_convert_card_data_creature(self):
        """Test card data conversion for creature with power/toughness."""
        api_data = {
            "id": "3",
            "name": "Lightning Elemental",
            "manaCost": "{3}{R}",
            "cmc": 4,
            "colors": ["Red"],
            "colorIdentity": ["R"],
            "type": "Creature — Elemental",
            "supertypes": [],
            "types": ["Creature"],
            "subtypes": ["Elemental"],
            "text": "Haste",
            "power": "4",
            "toughness": "1",
            "set": "M20",
            "setName": "Core Set 2020",
            "rarity": "Common",
        }

        card = convert_card_data(api_data)

        assert card.power == "4"
        assert card.toughness == "1"
        assert card.types == ["Creature"]
        assert card.subtypes == ["Elemental"]

    def test_convert_set_data_complete(self):
        """Test set data conversion with all fields."""
        api_data = {
            "code": "LEA",
            "name": "Limited Edition Alpha",
            "type": "Core",
            "releaseDate": "1993-08-05",
            "block": "Core Set",
            "onlineOnly": False,
            "cardCount": 295,
        }

        set_obj = convert_set_data(api_data)

        assert isinstance(set_obj, Set)
        assert set_obj.code == "LEA"
        assert set_obj.name == "Limited Edition Alpha"
        assert set_obj.type == "Core"
        assert set_obj.release_date == "1993-08-05"
        assert set_obj.block == "Core Set"
        assert set_obj.online_only is False
        assert set_obj.card_count == 295

    def test_convert_set_data_minimal(self):
        """Test set data conversion with minimal fields."""
        api_data = {"code": "TST", "name": "Test Set"}

        set_obj = convert_set_data(api_data)

        assert isinstance(set_obj, Set)
        assert set_obj.code == "TST"
        assert set_obj.name == "Test Set"
        assert set_obj.type is None
        assert set_obj.release_date is None
        assert set_obj.block is None
        assert set_obj.online_only is False  # Default value
        assert set_obj.card_count is None

    def test_convert_set_data_online_only(self):
        """Test set data conversion for online-only set."""
        api_data = {"code": "ONL", "name": "Online Set", "onlineOnly": True}

        set_obj = convert_set_data(api_data)

        assert set_obj.online_only is True
