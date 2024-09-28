from fastapi import APIRouter, Request
from api.controllers.telegram_controller import process_telegram_message

router = APIRouter()

@router.post("/telegram/message")
async def receive_telegram_message(request: Request):
    message = await request.json()
    response = await process_telegram_message(message)
    return response