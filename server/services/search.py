import logging
import httpx

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def search(self, query: str, model_types: str = "cards,boards"):
        """
        Search Trello for cards, boards, etc.
        """
        response = await self.client.GET(
            "/search",
            params={
                "query": query,
                "modelTypes": model_types,
                "partial": "true",
                "cards_limit": 20,
                "boards_limit": 20
            }
        )
        return response
