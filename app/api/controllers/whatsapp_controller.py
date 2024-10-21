from app.api.adapters.adapter_factory import get_adapter
from app.api.services.conversation_service import save_message_in_conversation
from app.api.services.message_transformer import transform_message
from fastapi.responses import JSONResponse


async def process_whatsapp_message(full_message: dict) -> JSONResponse:
    """Process a message from WhatsApp."""
    try:
        transformed_message = transform_message(full_message, "whatsapp")
        
        message_id = save_message_in_conversation(transformed_message)
        
        transformed_message.message_id = message_id
        
        # Further processing or sending to Celery
        # ...
        
        return JSONResponse(content={"status": "success", "message_id": message_id}, status_code=200)
    except Exception as e:
        # Error handling
        raise
