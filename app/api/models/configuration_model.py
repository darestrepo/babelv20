from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ConfigurationModel(BaseModel):
    platform: str = Field(description="Platform identifier (e.g., whatsapp, scala360)")
    token: str = Field(description="Authentication token for the platform")
    webhook_url: Optional[str] = Field(default=None, description="Webhook URL for the platform")
    conversation_id: Optional[str] = Field(default=None, description="Conversation identifier")
    sender_id: Optional[str] = Field(default=None, description="Sender's unique identifier")
    receiver_id: Optional[str] = Field(default=None, description="Receiver's unique identifier")
    additional_params: Dict[str, Any] = Field(default_factory=dict, description="Additional configuration parameters")
