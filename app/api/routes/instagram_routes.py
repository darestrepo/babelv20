from fastapi import APIRouter, Request
from app.api.controllers.instagram_controller import process_instagram_message
from app.api.services.routes.routesServices import requestFullMessageCreator

router = APIRouter()

@router.post("/instagram/message")
async def receive_instagram_message(request: Request):
    """Receive a message from Instagram."""
    full_message = await requestFullMessageCreator(request)
    response = await process_instagram_message(full_message)
    return response
