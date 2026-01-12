import logging
from typing import List, Dict, Any, Optional, Union

from server.trello import TrelloClient

logger = logging.getLogger(__name__)

class CustomFieldService:
    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_board_custom_fields(self, board_id: str) -> List[Dict[str, Any]]:
        """Get all custom field definitions for a board."""
        return await self.client.GET(f"/boards/{board_id}/customFields")

    async def get_card_custom_fields(self, card_id: str) -> List[Dict[str, Any]]:
        """Get all custom field items for a card."""
        return await self.client.GET(f"/cards/{card_id}/customFieldItems")

    async def update_card_custom_field(self, card_id: str, custom_field_id: str, value: Any) -> Dict[str, Any]:
        """
        Update a custom field value on a card.
        Value payload depends on the custom field type.
        """
        # The Trello API expects a specific object structure for the 'value' key
        # e.g., { "value": { "text": "Start Date" } } or { "value": { "number": "12" } }
        
        # We try to infer or let the caller pass the structured value?
        # To make it easy for the agent, we handle some basic types.
        
        payload = {}
        if isinstance(value, dict) and "value" in value:
             # Caller passed the full payload
            payload = value
        elif isinstance(value, dict):
            # Caller passed the inner value object
            payload = {"value": value}
        else:
             # Fallback, though typically custom fields need specific keys like text, number, checked, date, etc.
             # We'll assume text if it's a simple string, but this is risky without knowing the field type.
             # Ideally, the agent uses the schema from get_board_custom_fields.
             # For safety, let's require the caller to pass the dict with the type key.
             # e.g. {"text": "hello"}
             payload = {"value": value}

        return await self.client.PUT(
            f"/cards/{card_id}/customField/{custom_field_id}/item",
            data=payload
        )
