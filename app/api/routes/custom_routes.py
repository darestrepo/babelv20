from fastapi import APIRouter, Request
from app.api.controllers.custom_controller import process_custom_message
from app.api.services.routes.routesServices import requestFullMessageCreator

router = APIRouter()

@router.post("/custom/message")
async def receive_custom_message(request: Request):
    """Receive a message from a custom source."""
    full_message = await requestFullMessageCreator(request)
    response = await process_custom_message(full_message)
    return response
