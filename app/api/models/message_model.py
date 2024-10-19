from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MessageModel(BaseModel):
    """
    Universal message schema to standardize messages from all platforms.
    """
    message_id: str = Field(description="Unique identifier of the message")
    platform: str = Field(description="Originating platform identifier")
    sender_id: str = Field(description="Sender's unique identifier")
    receiver_id: Optional[str] = Field(default=None, description="Receiver's unique identifier")
    timestamp: str = Field(description="Message timestamp in ISO 8601 format")
    message_type: str = Field(description="Type of the message (text, media, interactive, etc.)")
    content: Optional[str] = Field(default=None, description="Text content of the message")
    media: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="List of media contents"
    )
    interactive: Optional[Dict[str, Any]] = Field(
        default=None, description="Interactive elements like buttons or lists"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data including headers, query params, and platform-specific information"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message_id": "msg123",
                    "platform": "scala360",
                    "sender_id": "+1234567890",
                    "receiver_id": "+0987654321",
                    "timestamp": "2023-10-15T14:30:00Z",
                    "message_type": "text",
                    "content": "Hello, how are you?",
                    "metadata": {
                        "headers": {
                            "conversation_token": "token123",
                            "unique_identifier": "unique123"
                        },
                        "query_params": {
                            "default_box": "box1",
                            "auth": "auth123"
                        }
                    }
                }
            ]
        }
    }
