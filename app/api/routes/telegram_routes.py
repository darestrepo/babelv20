from fastapi import APIRouter, Request
from app.api.controllers.telegram_controller import process_telegram_message
from app.api.services.routes.routesServices import requestFullMessageCreator

router = APIRouter()

@router.post("/telegram/message")
async def receive_telegram_message(request: Request):
    """Receive a message from Telegram."""
    full_message = await requestFullMessageCreator(request)
    response = await process_telegram_message(full_message)
    return response
