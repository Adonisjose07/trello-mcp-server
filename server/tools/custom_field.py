import logging
from typing import List, Dict, Any, Union

from mcp.server.fastmcp import Context

from server.services.custom_field import CustomFieldService
from server.trello import client

logger = logging.getLogger(__name__)

service = CustomFieldService(client)

async def get_board_custom_field_definitions(ctx: Context, board_id: str) -> List[Dict[str, Any]]:
    """Retrieves all custom field definitions available on a specific board.
    
    Use this to understand what custom fields (and their IDs/types) are available 
    before trying to update them on a card.

    Args:
        board_id (str): The ID of the board.

    Returns:
        List[Dict]: A list of custom field definitions.
    """
    try:
        logger.info(f"Getting custom field definitions for board: {board_id}")
        result = await service.get_board_custom_fields(board_id)
        return result
    except Exception as e:
        error_msg = f"Failed to get board custom fields: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def get_card_custom_field_items(ctx: Context, card_id: str) -> List[Dict[str, Any]]:
    """Retrieves the values of custom fields set on a specific card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[Dict]: A list of custom field items (values).
    """
    try:
        logger.info(f"Getting custom field items for card: {card_id}")
        result = await service.get_card_custom_fields(card_id)
        return result
    except Exception as e:
        error_msg = f"Failed to get card custom fields: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def update_card_custom_field_value(
    ctx: Context, 
    card_id: str, 
    custom_field_id: str, 
    value: Dict[str, Any]
) -> Dict[str, Any]:
    """Updates a custom field value on a card.

    Args:
        card_id (str): The ID of the card.
        custom_field_id (str): The ID of the custom field definition.
        value (Dict[str, Any]): The value to set, structured by type.
            Examples:
            - Text: {"text": "High Priority"}
            - Number: {"number": "42"}
            - Checkbox: {"checked": "true"}
            - Date: {"date": "2023-12-31T12:00:00.000Z"}
            - List: {"idValue": "opt_123..."} (for Dropdowns)

    Returns:
        Dict: The response from the update operation.
    """
    try:
        logger.info(f"Updating custom field {custom_field_id} on card {card_id} with value: {value}")
        result = await service.update_card_custom_field(card_id, custom_field_id, value)
        return result
    except Exception as e:
        error_msg = f"Failed to update custom field: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
