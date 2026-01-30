from typing import Optional
from pydantic import BaseModel, Field

class UpdateBoardPayload(BaseModel):
    """Payload for updating a Trello board."""
    name: Optional[str] = Field(None, description="The new name of the board.")
    desc: Optional[str] = Field(None, description="The new description of the board.")
    closed: Optional[bool] = Field(None, description="Whether the board is archived/closed.")
    prefs_background: Optional[str] = Field(None, description="The background color or image for the board.")
