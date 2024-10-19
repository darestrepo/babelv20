from typing import Dict
from app.api.adapters.platform_adapter import PlatformAdapter
from app.api.models.message_model import MessageModel
from app.api.models.configuration_model import ConfigurationModel  # Add this import

class Scala360Adapter(PlatformAdapter):
    """
    Adapter for Scala360 platform.
    Handles conversion between Scala360-specific messages and the universal format.
    """

    def to_universal(self, platform_message: Dict) -> MessageModel:
        """
        Convert Scala360 message to universal MessageModel.
        """
        message = platform_message["message"]
        headers = platform_message["headers"]
        query_params = platform_message["query_params"]

        return MessageModel(
            message_id=message.get("id"),
            platform="scala360",
            sender_id=message.get("owner"),
            receiver_id=message.get("conversation_id"),
            timestamp=message.get("created_at"),
            message_type=message.get("type"),
            content=message.get("content"),
            media=message.get("mediaUrl"),
            interactive=None,  # Adjust if Scala360 supports interactive elements
            metadata={
                "headers": headers,
                "query_params": query_params,
                "original_message": message
            }
        )

    def from_universal(self, universal_message: MessageModel) -> Dict:
        """
        Convert universal MessageModel to Scala360-specific message.
        """
        # Extract the original Scala360 message structure from metadata
        original_message = universal_message.metadata.get("original_message", {})
        
        # Update only the necessary fields
        original_message.update({
            "id": universal_message.message_id,
            "owner": universal_message.sender_id,
            "conversation_id": universal_message.receiver_id,
            "created_at": universal_message.timestamp,
            "type": universal_message.message_type,
            "content": universal_message.content,
            "mediaUrl": universal_message.media,
        })

        return original_message

    def send_message(self, universal_message: MessageModel, config: ConfigurationModel):
        """
        Sends a message to Scala360 using the provided configuration.
        """
        import requests

        scala_message = self.from_universal(universal_message)
        headers = {
            'Authorization': f'Bearer {config.token}',
            'Content-Type': 'application/json',
            'conversation-token': config.additional_params.get('conversation_token'),
            'unique-identifier': config.additional_params.get('unique_identifier')
        }
        response = requests.post(config.webhook_url, json=scala_message, headers=headers)
        response.raise_for_status()
        return response.json()
