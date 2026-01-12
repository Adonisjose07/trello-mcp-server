import logging
from typing import List, Dict, Any, Optional

from server.trello import TrelloClient

logger = logging.getLogger(__name__)

class AttachmentService:
    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_attachments(self, card_id: str) -> List[Dict[str, Any]]:
        """Get all attachments for a card."""
        return await self.client.GET(f"/cards/{card_id}/attachments")

    async def get_attachment(self, card_id: str, attachment_id: str) -> Dict[str, Any]:
        """Get a specific attachment."""
        return await self.client.GET(f"/cards/{card_id}/attachments/{attachment_id}")

    async def add_attachment(self, card_id: str, url: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Add an attachment to a card via URL."""
        payload = {"url": url}
        if name:
            payload["name"] = name
            
        return await self.client.POST(f"/cards/{card_id}/attachments", data=payload)

    async def delete_attachment(self, card_id: str, attachment_id: str) -> bool:
        """Delete an attachment from a card."""
        await self.client.DELETE(f"/cards/{card_id}/attachments/{attachment_id}")
        return True
