from api.services.message_transformer import transform_message
from api.services.message_dispatcher import dispatch_message
from api.models.message_model import MessageModel

async def process_instagram_message(message: dict):
    message_model = MessageModel(**message)
    standardized_message = transform_message(message_model.dict(), platform="instagram")
    dispatch_message(standardized_message)
    return {"status": "Message received and is being processed."}