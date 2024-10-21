from typing import Dict
from app.api.adapters.platform_adapter import PlatformAdapter
from app.api.models.message_model import MessageModel

class WhatsappAdapter(PlatformAdapter):
    """
    Adapter for WhatsApp platform.
    Handles conversion between WhatsApp-specific messages and the universal format.
    """

    def to_universal(self, platform_message: Dict) -> MessageModel:
        """
        Convert WhatsApp message to universal MessageModel.
        """
        message = platform_message["message"]
        headers = platform_message["headers"]
        query_params = platform_message["query_params"]

        return MessageModel(
            message_id=message.get("id"),
            platform="whatsapp",
            sender_id=message.get("from"),
            receiver_id=message.get("to"),
            timestamp=message.get("timestamp"),
            message_type=message.get("type"),
            content=message.get("text", {}).get("body"),
            media=message.get("media"),
            interactive=None,  # Adjust if WhatsApp supports interactive elements
            metadata={
                "headers": headers,
                "query_params": query_params,
                "original_message": message
            }
        )

    def from_universal(self, universal_message: MessageModel) -> Dict:
        """
        Convert universal MessageModel to WhatsApp-specific message.
        """
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": universal_message.receiver_id,
            "type": universal_message.message_type,
            universal_message.message_type: {
                "preview_url": True,
                "body": universal_message.content
            }
        }

    def send_message(self, universal_message: MessageModel, config: Dict):
        """
        Sends a message to WhatsApp using the provided configuration.
        """
        # Implement the send logic
        pass
