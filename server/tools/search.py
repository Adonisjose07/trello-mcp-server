import logging
from typing import Dict, Any, List

from mcp.server.fastmcp import Context
from server.services.search import SearchService
from server.trello import client

logger = logging.getLogger(__name__)

service = SearchService(client)

async def search_trello(ctx: Context, query: str) -> Dict[str, Any]:
    """
    Search for Trello cards and boards using a query string.
    
    Args:
        query (str): The text to search for.
        
    Returns:
        Dict: Search results containing lists of cards and boards.
    """
    try:
        logger.info(f"Searching Trello for: {query}")
        result = await service.search(query)
        logger.info(f"Search completed for: {query}")
        return {
            "cards": result.get("cards", []),
            "boards": result.get("boards", [])
        }
    except Exception as e:
        error_msg = f"Search failed: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
