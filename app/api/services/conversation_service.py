from app.api.services.redis.redis_service import create_conversation, add_message_to_conversation, get_messages_from_conversation
from app.api.models.message_model import MessageModel
from typing import List, Dict, Any

def save_message_in_conversation(message: MessageModel) -> str:
    """
    Manages a conversation by creating or updating it in Redis.
    
    This function will:
    1. Create or get the conversation key (this now preserves existing conversations)
    2. Add the new message to the conversation
    3. Return the message ID
    
    Args:
        message (MessageModel): The message to add to the conversation.
        
    Returns:
        str: The unique ID of the added message.
    """
    # Create or get the conversation key (this now preserves existing conversations)
    conversation_key = create_conversation(message.chat_conversation_id)
    # Add the message to the conversation
    message_id = add_message_to_conversation(conversation_key, message)
    
    return message_id


def get_conversation_history(message: MessageModel) -> List[Dict[str, Any]]:
    """
    Retrieves the conversation history for a specific tenant, receiver, and sender.
    
    Args:
        message (MessageModel): A message containing tenant_id, receiver_id, and sender_id.
        
    Returns:
        List[Dict[str, Any]]: A list of messages in the conversation.
    """
    conversation_key = f"chat:{message.tenant_id}:{message.receiver_id}:{message.sender_id}"
    return get_messages_from_conversation(conversation_key)
