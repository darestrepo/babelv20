from datetime import datetime, timezone
from dotenv import load_dotenv
import redis
import json
import os
import uuid
from typing import List, Dict, Any, Optional
from app.api.models.message_model import MessageModel

load_dotenv()


app_secret = os.getenv('APP_SECRET')
secret = json.loads(app_secret)
redis_url = secret["REDIS_HOST"]
redis_port = secret["REDIS_PORT"]
redis_db = secret["REDIS_DB"]
stage = secret["STAGE"]

pool = redis.ConnectionPool(host=redis_url, port=redis_port, db=redis_db)
r = redis.Redis(connection_pool=pool)



def create_conversation(chat_conversation_id: str) -> str:
    """
    Create a unique Redis key for a conversation or return an existing one,
    and ensure its TTL is set to 26 hours.
    
    Args:
        chat_conversation_id (str): The chat conversation identifier.

    Returns:
        str: The Redis key for the conversation.
    """
    key = chat_conversation_id
    
    # Check if the key already exists
    if not r.exists(key):
        # If it doesn't exist, initialize it with a conversation start message
        r.rpush(key, json.dumps({"type": "conversation_start", "timestamp": datetime.now(timezone.utc).isoformat()}))
    
    # Regardless of whether it existed or not, reset the TTL to 26 hours
    r.expire(key, 26 * 3600)
    
    return key


def add_message_to_conversation(key: str, message: MessageModel) -> str:
    """
    Add a message to a conversation and reset the conversation's TTL to 26 hours.
    
    Args:
        key (str): The Redis key for the conversation.
        message (MessageModel): The message to add.
        
    Returns:
        str: The unique ID of the added message.
    """
    message_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Convert MessageModel to a dictionary, excluding None values
    message_dict = message.model_dump(exclude_none=True)
    
    # Create the Redis entry
    redis_entry = {
        "id": message_id,
        "timestamp": timestamp,
        "content": message_dict
    }
    
    r.rpush(key, json.dumps(redis_entry))
    r.expire(key, 26 * 3600)  # Reset TTL to 26 hours
    return message_id


def get_messages_from_conversation(key: str) -> List[Dict[str, Any]]:
    """
    Retrieve all messages from a conversation that are within the last 26 hours.
    
    Args:
        key (str): The Redis key for the conversation.
        
    Returns:
        List[Dict[str, Any]]: A list of messages.
    """
    messages = r.lrange(key, 0, -1)
    return [json.loads(msg.decode('utf-8')) for msg in messages]


def get_messages_as_models(key: str) -> List[MessageModel]:
    """
    Retrieve all messages from a conversation and convert them to MessageModel objects.
    
    Args:
        key (str): The Redis key for the conversation.
        
    Returns:
        List[MessageModel]: A list of MessageModel objects.
    """
    messages = get_messages_from_conversation(key)
    return [MessageModel(**msg['content']) for msg in messages]


def get_last_message_from_conversation(key: str) -> Optional[MessageModel]:
    """
    Retrieve the last message from a conversation and convert it to a MessageModel object.
    
    Args:
        key (str): The Redis key for the conversation.
        
    Returns:
        Optional[MessageModel]: The last message as a MessageModel object, or None if the conversation is empty.
    """
    last_message = r.lindex(key, -1)
    if last_message is None:
        return None
    
    message_dict = json.loads(last_message.decode('utf-8'))
    return MessageModel(**message_dict['content'])


def get_message_by_id(chat_conversation_id: str, message_id: str) -> Optional[MessageModel]:
    """
    Retrieve a specific message from a conversation by its message_id.

    Args:
        chat_conversation_id (str): The Redis key for the conversation.
        message_id (str): The unique identifier of the message to retrieve.

    Returns:
        Optional[MessageModel]: The message as a MessageModel object if found, None otherwise.
    """
    messages = r.lrange(chat_conversation_id, 0, -1)
    for msg in reversed(messages):
        message_dict = json.loads(msg.decode('utf-8'))
        if message_dict['id'] == message_id:
            return MessageModel(**message_dict['content'])
    return None

