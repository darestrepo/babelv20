from pydantic import BaseModel
from typing import Optional

class MessageModel(BaseModel):
    user_id: str
    content: str
    timestamp: Optional[str]