from fastapi import APIRouter, Request
from app.api.controllers.messenger_controller import process_messenger_message
from app.api.services.routes.routesServices import requestFullMessageCreator

router = APIRouter()

@router.post("/messenger/message")
async def receive_messenger_message(request: Request):
    """Receive a message from Messenger."""
    full_message = await requestFullMessageCreator(request)
    response = await process_messenger_message(full_message)
    return response
