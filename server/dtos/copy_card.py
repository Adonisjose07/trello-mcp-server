from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class CopyCardPayload(BaseModel):
    """Payload for cloning/copying a Trello card."""
    idCardSource: str = Field(..., description="The ID of the card to copy.")
    idList: str = Field(..., description="The ID of the target list for the new card.")
    name: Optional[str] = Field(None, description="Optional new name for the copied card.")
    desc: Optional[str] = Field(None, description="Optional new description for the copied card.")
    keepFromSource: Optional[str] = Field("all", description="Components to keep from source (all, attachments, checkitems, comments, labels, members, stickers).")
