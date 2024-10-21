from app.api.adapters.adapter_factory import get_adapter
from app.api.services.message_transformer import transform_message
from fastapi.responses import JSONResponse


async def process_instagram_message(full_message: dict) -> JSONResponse:
    """Process a message from Instagram."""
    try:
        transformed_message = transform_message(full_message, "instagram")
        adapter = get_adapter("instagram")
        response = await adapter.process_message(transformed_message)
        return response
    except Exception as e:
        raise
