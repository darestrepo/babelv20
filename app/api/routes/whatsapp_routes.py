from fastapi import APIRouter, Request
from app.api.controllers.whatsapp_controller import process_whatsapp_message
from app.api.services.routes.routesServices import requestFullMessageCreator

router = APIRouter()


@router.post("/message")
async def receive_whatsapp_message(request: Request):
    """Receive a message from Whatsapp."""
    full_message = await requestFullMessageCreator(request)
    response = await process_whatsapp_message(full_message)
    return response
