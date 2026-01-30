"""
Service for managing Trello boards in MCP server.
"""

from typing import List

from server.models import TrelloBoard, TrelloLabel, TrelloMember, TrelloWorkspace
from server.utils.trello_api import TrelloClient


class BoardService:
    """
    Service class for managing Trello boards
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_board(self, board_id: str) -> TrelloBoard:
        """Retrieves a specific board by its ID."""
        response = await self.client.GET(f"/boards/{board_id}")
        return TrelloBoard(**response)

    async def get_boards(self, member_id: str = "me", filter: str = "open") -> List[TrelloBoard]:
        """Retrieves all boards for a given member.
        
        Args:
            member_id (str): The ID of the member. Defaults to "me".
            filter (str): Filter for board status. Can be 'all', 'closed', 'members', 'open', 'organization', 'public', 'starred'.
        """
        params = {"filter": filter}
        response = await self.client.GET(f"/members/{member_id}/boards", params=params)
        return [TrelloBoard(**board) for board in response]

    async def get_workspaces(self) -> List[TrelloWorkspace]:
        """Retrieves all workspaces (organizations) for the authenticated user."""
        response = await self.client.GET("/members/me/organizations")
        return [TrelloWorkspace(**ws) for ws in response]

    async def get_workspace_boards(self, workspace_id: str, filter: str = "open") -> List[TrelloBoard]:
        """Retrieves all boards within a specific workspace.
        
        Args:
            workspace_id (str): The ID of the workspace.
            filter (str): Filter for board status.
        """
        params = {"filter": filter}
        response = await self.client.GET(f"/organizations/{workspace_id}/boards", params=params)
        return [TrelloBoard(**board) for board in response]

    async def get_board_labels(self, board_id: str) -> List[TrelloLabel]:
        """Retrieves all labels for a specific board.

        Args:
            board_id (str): The ID of the board whose labels to retrieve.

        Returns:
            List[TrelloLabel]: A list of label objects for the board.
        """
        response = await self.client.GET(f"/boards/{board_id}/labels")
        return [TrelloLabel(**label) for label in response]

    async def create_board_label(self, board_id: str, **kwargs) -> TrelloLabel:
        """Create label for a specific board.

        Args:
            board_id (str): The ID of the board whose to add label.

        Returns:
            List[TrelloLabel]: A list of label objects for the board.
        """
        response = await self.client.POST(f"/boards/{board_id}/labels", data=kwargs)
        return TrelloLabel(**response)

    async def get_board_members(self, board_id: str) -> List[TrelloMember]:
        """Retrieves all members for a specific board.

        Args:
            board_id (str): The ID of the board whose members to retrieve.

        Returns:
            List[TrelloMember]: A list of member objects.
        """
        response = await self.client.GET(f"/boards/{board_id}/members")
        # Note: Trello API usually returns basic fields. 'email' might be missing dependent on permissions.
        # We pass the data to the model, allowing optional fields to be None.
        return [TrelloMember(**member) for member in response]
