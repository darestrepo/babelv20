from fastapi import APIRouter, Request
from api.controllers.messenger_controller import process_messenger_message

router = APIRouter()

@router.post("/messenger/message")
async def receive_messenger_message(request: Request):
    message = await request.json()
    response = await process_messenger_message(message)
    return response