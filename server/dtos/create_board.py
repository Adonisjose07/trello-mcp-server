from typing import Optional
from pydantic import BaseModel, Field

class CreateBoardPayload(BaseModel):
    """Payload for creating a new Trello board."""
    name: str = Field(..., description="The name of the new board.")
    desc: Optional[str] = Field(None, description="Optional description of the board.")
    idOrganization: Optional[str] = Field(None, description="The ID of the workspace (organization) to create the board in.")
    defaultLists: Optional[bool] = Field(True, description="Whether to create the default lists (To Do, Doing, Done).")
    prefs_background: Optional[str] = Field("blue", description="The background color or image for the board.")
    prefs_permissionLevel: Optional[str] = Field("private", description="The permission level of the board (private, org, public).")
