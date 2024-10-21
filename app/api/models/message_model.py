from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class OriginalMessage(BaseModel):
    """
    Original message is the message as was received from the platform
    """
    headers: Dict[str, Any] = Field(default_factory=dict, description="Headers")
    query_params: Dict[str, Any] = Field(default_factory=dict, description="Query params")
    message: Dict[str, Any] = Field(default_factory=dict, description="Message")

class Metadata(BaseModel):
    """
    Metadata is additional data added to the Universal message schema
    """
    original_message: OriginalMessage = Field(description="Original message from the platform")
    required_fields: Dict[str, Any] = Field(default_factory=dict, description="Required fields to answer the message in the destination channel")

class MessageModel(BaseModel):
    """
    Universal message schema to standardize messages from all platforms.
    """
    message_id: Optional[str] = Field(default=None, description="Message ID")
    chat_conversation_id: str = Field(default=None, description="Unique identifier for the chat conversation")
    conversation_id: str = Field(default=None, description="Unique identifier for the conversation")
    platform: str = Field(description="Originating platform identifier")
    user_name: Optional[str] = Field(default=None, description="User name")
    tenant_id: str = Field(description="Tenant ID")
    sender_id: str = Field(description="Sender's unique identifier")
    receiver_id: Optional[str] = Field(default=None, description="Receiver's unique identifier")
    timestamp: str = Field(description="Message timestamp in ISO 8601 format")
    messages: List[Dict[str, Any]] = Field(description="List of messages, each containing type (text, media, interactive, etc.) and content")
    metadata: Metadata = Field(description="Metadata")

    def __init__(self, **data):
        super().__init__(**data)
        self._set_chat_conversation_id()

    def _set_chat_conversation_id(self) -> None:
        """
        Set the chat_conversation_id if tenant_id, receiver_id, and sender_id are present.
        """
        if self.tenant_id and self.receiver_id and self.sender_id:
            self.chat_conversation_id = f"chat:{self.tenant_id}:{self.receiver_id}:{self.sender_id}"
            self.conversation_id = f"{self.tenant_id}_{self.receiver_id}_{self.sender_id}"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message_id": "1234567890",
                    "chat_conversation_id": "chat:121:1234567890:573204917701",
                    "conversation_id": "121_1234567890_573204917701",
                    "platform": "scala360",
                    "tenant_id": "121",
                    "sender_id": "1234567890",
                    "receiver_id": "573204917701",
                    "timestamp": "2023-10-15T14:30:00Z",
                    "messages": [
                        {
                            "message_type": "text",
                            "text": {
                                "body": "Hola Kanaryo"
                            }
                        }
                    ],
                    "metadata": {
                        "original_message": {
                            "headers": {
                                "conversation_token": "token123",
                                "unique_identifier": "unique123"
                            },
                            "query_params": {
                                "default_box": "36421",
                                "auth": "auth123"
                            },
                            "message": {
                                'type': 'text', 
                                'content': '1', 
                                'owner': '573204917701', 
                                'is_bot': False, 
                                'company_id': 121, 
                                'direction': 'incoming', 
                                'message_uuid': 'Zf4vm2YzWKFziQAKEbnPujzneeffX8B0lOgFkKx7', 
                                'conversation_id': 137516977
                            }
                        },
                        "nextStateId": "1234567890",
                        "conversation-token": "gLIHQePAxN",
                        "authorization": "Bearer 1234567890",
                        'slug': 'virtualllantas', 
                        'agent_campaing_box': '34474058'
                    }
                }
            ]
        }
    }
