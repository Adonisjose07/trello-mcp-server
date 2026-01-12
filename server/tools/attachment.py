import logging
from typing import List, Dict, Any, Optional

from mcp.server.fastmcp import Context

from server.services.attachment import AttachmentService
from server.trello import client

logger = logging.getLogger(__name__)

service = AttachmentService(client)

async def get_card_attachments(ctx: Context, card_id: str) -> List[Dict[str, Any]]:
    """Retrieves all attachments for a specific card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[Dict]: A list of attachment objects.
    """
    try:
        logger.info(f"Getting attachments for card: {card_id}")
        result = await service.get_attachments(card_id)
        return result
    except Exception as e:
        error_msg = f"Failed to get attachments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def add_attachment_to_card(ctx: Context, card_id: str, url: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Adds an attachment to a card using a URL.

    Args:
        card_id (str): The ID of the card.
        url (str): The URL of the attachment.
        name (str, optional): The name of the attachment.

    Returns:
        Dict: The created attachment object.
    """
    try:
        logger.info(f"Adding attachment to card {card_id}: {url}")
        result = await service.add_attachment(card_id, url, name)
        return result
    except Exception as e:
        error_msg = f"Failed to add attachment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def delete_attachment_from_card(ctx: Context, card_id: str, attachment_id: str) -> bool:
    """Deletes an attachment from a card.

    Args:
        card_id (str): The ID of the card.
        attachment_id (str): The ID of the attachment to delete.

    Returns:
        bool: True if successful.
    """
    try:
        logger.info(f"Deleting attachment {attachment_id} from card: {card_id}")
        await service.delete_attachment(card_id, attachment_id)
        return True
    except Exception as e:
        error_msg = f"Failed to delete attachment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
