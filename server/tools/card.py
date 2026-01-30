"""
This module contains tools for managing Trello cards.
"""

import logging
from typing import List, Dict, Any

from mcp.server.fastmcp import Context

from server.models import TrelloCard
from server.services.card import CardService
from server.trello import client
from server.dtos.update_card import UpdateCardPayload
from server.dtos.create_card import CreateCardPayload
from server.dtos.copy_card import CopyCardPayload
from server.utils.auth import require_write_access

logger = logging.getLogger(__name__)

service = CardService(client)


async def get_card(ctx: Context, card_id: str) -> TrelloCard:
    """Retrieves a specific card by its ID.

    Args:
        card_id (str): The ID of the card to retrieve.

    Returns:
        TrelloCard: The card object containing card details.
    """
    try:
        logger.info(f"Getting card with ID: {card_id}")
        result = await service.get_card(card_id)
        logger.info(f"Successfully retrieved card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_cards(ctx: Context, list_id: str) -> List[TrelloCard]:
    """Retrieves all cards in a given list.

    Args:
        list_id (str): The ID of the list whose cards to retrieve.

    Returns:
        List[TrelloCard]: A list of card objects.
    """
    try:
        logger.info(f"Getting cards for list: {list_id}")
        result = await service.get_cards(list_id)
        logger.info(f"Successfully retrieved {len(result)} cards for list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get cards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def create_card(ctx: Context, payload: CreateCardPayload) -> TrelloCard:
    """Creates a new card in a given list.

    Args:
        list_id (str): The ID of the list to create the card in.
        name (str): The name of the new card.
        desc (str, optional): The description of the new card. Defaults to None.

    Returns:
        TrelloCard: The newly created card object.
    """
    try:
        logger.info(f"Creating card in list {payload.idList} with name: {payload.name}")
        result = await service.create_card(**payload.model_dump(exclude_unset=True))
        logger.info(f"Successfully created card in list: {payload.idList}")
        return result
    except Exception as e:
        error_msg = f"Failed to create card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def update_card(
    ctx: Context, card_id: str, payload: UpdateCardPayload
) -> TrelloCard:
    """Updates a card's attributes.

    Args:
        card_id (str): The ID of the card to update.
        **kwargs: Keyword arguments representing the attributes to update on the card.

    Returns:
        TrelloCard: The updated card object.
    """
    try:
        logger.info(f"Updating card: {card_id} with payload: {payload}")
        result = await service.update_card(
            card_id, **payload.model_dump(exclude_unset=True)
        )
        logger.info(f"Successfully updated card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def delete_card(ctx: Context, card_id: str) -> dict:
    """Deletes a card.

    Args:
        card_id (str): The ID of the card to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting card: {card_id}")
        result = await service.delete_card(card_id)
        logger.info(f"Successfully deleted card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def get_card_comments(ctx: Context, card_id: str) -> List[Dict[str, Any]]:
    """Retrieves all comments for a specific card.

    Args:
        card_id (str): The ID of the card.

    Returns:
        List[Dict]: A list of comment actions.
    """
    try:
        logger.info(f"Getting comments for card: {card_id}")
        result = await service.get_comments(card_id)
        logger.info(f"Successfully retrieved comments for card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get card comments: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def add_comment_to_card(ctx: Context, card_id: str, text: str) -> Dict[str, Any]:
    """Adds a new comment to a card.

    Args:
        card_id (str): The ID of the card.
        text (str): The comment text.

    Returns:
        Dict: The created comment action.
    """
    try:
        logger.info(f"Adding comment to card: {card_id}")
        result = await service.add_comment(card_id, text)
        logger.info(f"Successfully added comment to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add comment: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

@require_write_access
async def add_member_to_card(ctx: Context, card_id: str, member_id: str) -> List[Dict[str, Any]]:
    """Adds a member to a card.

    Args:
        card_id (str): The ID of the card.
        member_id (str): The ID of the member to add.

    Returns:
        List[Dict]: The updated list of members on the card.
    """
    try:
        logger.info(f"Adding member {member_id} to card: {card_id}")
        result = await service.add_member(card_id, member_id)
        logger.info(f"Successfully added member to card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to add member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def remove_member_from_card(ctx: Context, card_id: str, member_id: str) -> List[Dict[str, Any]]:
    """Removes a member from a card.

    Args:
        card_id (str): The ID of the card.
        member_id (str): The ID of the member to remove.

    Returns:
        List[Dict]: The updated list of members on the card.
    """
    try:
        logger.info(f"Removing member {member_id} from card: {card_id}")
        result = await service.remove_member(card_id, member_id)
        logger.info(f"Successfully removed member from card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to remove member: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def copy_card(ctx: Context, payload: CopyCardPayload) -> TrelloCard:
    """Clones an existing Trello card to a new list.

    Args:
        payload (CopyCardPayload): Details for cloning the card.

    Returns:
        TrelloCard: The newly created (cloned) card object.
    """
    try:
        logger.info(f"Copying card {payload.idCardSource} to list {payload.idList}")
        result = await service.copy_card(**payload.model_dump(exclude_unset=True))
        logger.info(f"Successfully copied card to: {result.id}")
        return result
    except Exception as e:
        error_msg = f"Failed to copy card: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
