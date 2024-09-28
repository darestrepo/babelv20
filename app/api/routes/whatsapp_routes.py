from fastapi import APIRouter, Request
from api.controllers.whatsapp_controller import process_whatsapp_message

router = APIRouter()

@router.post("/message")
async def receive_whatsapp_message(request: Request):
    message = await request.json()
    response = await process_whatsapp_message(message)
    return response