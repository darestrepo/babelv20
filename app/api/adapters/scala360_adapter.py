from typing import Dict
from app.api.adapters.platform_adapter import PlatformAdapter
from app.api.models.message_model import MessageModel, Metadata, OriginalMessage
from app.api.models.configuration_model import ConfigurationModel
from datetime import datetime


class Scala360Adapter(PlatformAdapter):
    """
    Adapter for Scala360 platform.
    Handles conversion between Scala360-specific messages and the universal format.
    """

    def to_universal(self, full_message: Dict) -> MessageModel:
        """
        Convert Scala360 message to universal MessageModel.
        """
        message = full_message["message"]
        headers = full_message["headers"]
        query_params = full_message["query_params"]
        
        original_message = OriginalMessage(
            headers=headers,
            query_params=query_params,
            message=message
        )

        required_fields = {
            "nextStateId": message.get("default_box", None),
            "conversation-token": headers.get("conversation-token", None),
            "authorization": headers.get("authorization", None),
            'slug': message.get("slug", None), 
            'agent_campaing_box': message.get("agent_campaing_box", None),
            'scala_auth': message.get("auth", None),
            'meta_auth': headers.get("authorization", None)
        }

        metadata = Metadata(
            original_message=original_message,
            required_fields=required_fields
        )

        messages = messages_content_creator(message)

        return MessageModel(
            platform="scala360",
            user_name=message.get("message", {}).get("owner_name_wa", None),
            tenant_id=str(message.get("message", {}).get("company_id")),
            sender_id=message.get("message", {}).get("owner"),
            receiver_id=message.get("whatsapp_number"),
            timestamp=datetime.now().isoformat(),  # Use current time if not available
            messages=messages,
            metadata=metadata
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


def messages_content_creator(message: Dict) -> Dict:
    """
    Creates the content of the message to be sent to Scala360.
    """
    messages = []
    if message['message']['type'] == "text":
        messages.append(
            {
                "message_type": "text",
                "text": {
                    "body": message['message']['content']
                }
            }
        )

    #TODO: Add other message types
    else:
        pass
    
    return messages