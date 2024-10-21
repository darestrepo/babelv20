import sys
from app.api.adapters.adapter_factory import get_adapter
from app.api.models.message_model import MessageModel
from pydantic import BaseModel


class UniversalMessage(BaseModel):
    platform: str
    user_id: str
    content: str
    timestamp: str


def transform_message(full_message: dict, platform: str) -> MessageModel:
    """
    Transform a platform-specific message to the universal MessageModel format.
    """    
    try:
        adapter = get_adapter(platform)        
        universal_message = adapter.to_universal(full_message)
        return universal_message
    except Exception as e:
        print(f"Error in transform_message: {str(e)}", file=sys.stderr)
        raise


def transform_to_platform(universal_message: MessageModel, platform: str) -> dict:
    """
    Transform a universal MessageModel to a platform-specific message format.
    """
    adapter = get_adapter(platform)
    original_format_message = adapter.from_universal(universal_message)
    return original_format_message


def transform_response(response: dict, platform: str) -> dict:
    """
    Transform a response to the universal format.
    """
    adapter = get_adapter(platform)
    universal_message = adapter.to_universal(response)
    return universal_message.dict()
