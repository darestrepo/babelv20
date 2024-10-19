from app.api.adapters.adapter_factory import AdapterFactory
from pydantic import BaseModel

class UniversalMessage(BaseModel):
    platform: str
    user_id: str
    content: str
    timestamp: str

def transform_message(message: dict, platform: str) -> dict:
    adapter = AdapterFactory.get_adapter(platform)
    universal_message = adapter.to_universal(message)
    return universal_message.dict()

def transform_response(response: dict, platform: str) -> dict:
    adapter = AdapterFactory.get_adapter(platform)
    universal_message = adapter.from_universal(response)
    return universal_message
