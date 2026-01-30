"""
This module contains tools for managing Trello boards.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloBoard, TrelloLabel, TrelloMember, TrelloWorkspace
from server.dtos.create_label import CreateLabelPayload
from server.dtos.create_board import CreateBoardPayload
from server.dtos.update_board import UpdateBoardPayload
from server.services.board import BoardService
from server.trello import client
from server.utils.auth import require_write_access

logger = logging.getLogger(__name__)

service = BoardService(client)


async def get_board(ctx: Context, board_id: str) -> TrelloBoard:
    """Retrieves a specific board by its ID.

    Args:
        board_id (str): The ID of the board to retrieve.

    Returns:
        TrelloBoard: The board object containing board details.
    """
    try:
        logger.info(f"Getting board with ID: {board_id}")
        result = await service.get_board(board_id)
        logger.info(f"Successfully retrieved board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_boards(ctx: Context, filter: str = "open") -> List[TrelloBoard]:
    """Retrieves all boards for the authenticated user with optional filtering.

    Args:
        filter (str, optional): Filtering status of the boards. 
            Options: 'all' (includes invited), 'closed', 'members', 'open' (default), 'organization', 'public', 'starred'.

    Returns:
        List[TrelloBoard]: A list of board objects.
    """
    try:
        logger.info(f"Getting all boards with filter: {filter}")
        result = await service.get_boards(filter=filter)
        logger.info(f"Successfully retrieved {len(result)} boards")
        return result
    except Exception as e:
        error_msg = f"Failed to get boards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_workspaces(ctx: Context) -> List[TrelloWorkspace]:
    """Retrieves all Trello Workspaces (organizations) that the current user is a member of.

    Returns:
        List[TrelloWorkspace]: A list of workspace objects containing ID, name, and URL.
    """
    try:
        logger.info("Getting all workspaces")
        result = await service.get_workspaces()
        logger.info(f"Successfully retrieved {len(result)} workspaces")
        return result
    except Exception as e:
        error_msg = f"Failed to get workspaces: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_workspace_boards(ctx: Context, workspace_id: str, filter: str = "open") -> List[TrelloBoard]:
    """Retrieves all boards belonging to a specific Trello Workspace.

    Args:
        workspace_id (str): The ID of the workspace (organization).
        filter (str, optional): Filtering status of the boards. 
            Options: 'all', 'closed', 'members', 'open' (default), 'organization', 'public', 'starred'.

    Returns:
        List[TrelloBoard]: A list of board objects.
    """
    try:
        logger.info(f"Getting boards for workspace: {workspace_id} with filter: {filter}")
        result = await service.get_workspace_boards(workspace_id, filter=filter)
        logger.info(f"Successfully retrieved {len(result)} boards for workspace: {workspace_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get workspace boards: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_board_labels(ctx: Context, board_id: str) -> List[TrelloLabel]:
    """Retrieves all labels for a specific board.

    Args:
        board_id (str): The ID of the board whose labels to retrieve.

    Returns:
        List[TrelloLabel]: A list of label objects for the board.
    """
    try:
        logger.info(f"Getting labels for board: {board_id}")
        result = await service.get_board_labels(board_id)
        logger.info(f"Successfully retrieved {len(result)} labels for board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board labels: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


@require_write_access
async def create_board_label(ctx: Context, board_id: str, payload: CreateLabelPayload) -> TrelloLabel:
    """Create label for a specific board.

    Args:
        board_id (str): The ID of the board whose to add label to.
        name (str): The name of the label.
        color (str): The color of the label.

    Returns:
        TrelloLabel: A label object for the board.
    """
    try:
        logger.info(f"Creating label {payload.name} label for board: {board_id}")
        result = await service.create_board_label(board_id, **payload.model_dump(exclude_unset=True))
        logger.info(f"Successfully created label {payload.name} labels for board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board labels: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise


async def get_board_members(ctx: Context, board_id: str) -> List[TrelloMember]:
    """Retrieves all members for a specific board.
    
    Returns basic member info (name, username, id). Email might be available depending on permissions.

    Args:
        board_id (str): The ID of the board.

    Returns:
        List[TrelloMember]: List of members.
    """
    try:
        logger.info(f"Getting members for board: {board_id}")
        result = await service.get_board_members(board_id)
        logger.info(f"Successfully retrieved {len(result)} members for board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board members: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def get_me(ctx: Context) -> TrelloMember:
    """Retrieves the authenticated user's profile.
    
    Returns:
        TrelloMember: Your Trello profile information.
    """
    try:
        logger.info("Getting current user profile")
        result = await service.get_me()
        logger.info(f"Successfully retrieved profile for: {result.username}")
        return result
    except Exception as e:
        error_msg = f"Failed to get user profile: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

async def get_board_actions(ctx: Context, board_id: str, filter: str = "all", limit: int = 50) -> List[dict]:
    """Retrieves recent actions/activity for a Trello board.

    Args:
        board_id (str): The ID of the board.
        filter (str, optional): Action types to return. Defaults to 'all'.
        limit (int, optional): Maximum number of actions. Defaults to 50.

    Returns:
        List[dict]: A list of recent activities on the board.
    """
    try:
        logger.info(f"Getting actions for board: {board_id}")
        result = await service.get_board_actions(board_id, filter, limit)
        logger.info(f"Successfully retrieved {len(result)} actions for board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board actions: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

@require_write_access
async def create_board(ctx: Context, payload: CreateBoardPayload) -> TrelloBoard:
    """Creates a new Trello board.

    Args:
        payload (CreateBoardPayload): Details for the new board.

    Returns:
        TrelloBoard: The newly created board object.
    """
    try:
        logger.info(f"Creating board: {payload.name}")
        result = await service.create_board(**payload.model_dump(exclude_unset=True))
        logger.info(f"Successfully created board: {result.id}")
        return result
    except Exception as e:
        error_msg = f"Failed to create board: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

@require_write_access
async def update_board(ctx: Context, board_id: str, payload: UpdateBoardPayload) -> TrelloBoard:
    """Updates an existing Trello board.

    Args:
        board_id (str): The ID of the board to update.
        payload (UpdateBoardPayload): Attributes to update.

    Returns:
        TrelloBoard: The updated board object.
    """
    try:
        logger.info(f"Updating board: {board_id}")
        result = await service.update_board(board_id, **payload.model_dump(exclude_unset=True))
        logger.info(f"Successfully updated board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update board: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise

