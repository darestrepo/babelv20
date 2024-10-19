from typing import Dict
from app.api.adapters.platform_adapter import PlatformAdapter
from app.api.models.message_model import MessageModel
from app.api.models.configuration_model import ConfigurationModel

class WhatsAppAdapter(PlatformAdapter):
    """
    Adapter for WhatsApp platform.
    Handles conversion between WhatsApp-specific messages and the universal format.
    """

    def to_universal(self, platform_message: Dict) -> MessageModel:
        """
        Convert WhatsApp message to universal MessageModel.
        """
        return MessageModel(
            message_id=platform_message.get("id"),
            platform="whatsapp",
            sender_id=platform_message.get("from"),
            receiver_id=platform_message.get("to"),
            timestamp=platform_message.get("timestamp"),
            message_type=platform_message.get("type"),
            content=platform_message.get("text", {}).get("body"),
            media=platform_message.get("media"),
            interactive=None,  # WhatsApp may have interactive elements
            metadata=platform_message
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
        import requests

        whatsapp_message = self.from_universal(universal_message)
        headers = {
            'Authorization': f'Bearer {config["token"]}',
            'Content-Type': 'application/json'
        }
        response = requests.post(config['webhook_url'], json=whatsapp_message, headers=headers)
        response.raise_for_status()
        return response.json()
