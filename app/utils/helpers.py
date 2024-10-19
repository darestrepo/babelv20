from app.api.adapters.adapter_factory import AdapterFactory
from app.api.models.message_model import MessageModel

def send_outbound_message(standardized_message: dict, config: dict):
    adapter = AdapterFactory.get_adapter(standardized_message['platform'])
    universal_message = MessageModel(**standardized_message)
    adapter.send_message(universal_message, config)
