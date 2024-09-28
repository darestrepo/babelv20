from fastapi import APIRouter, Request
from api.controllers.custom_controller import process_custom_message

router = APIRouter()

@router.post("/custom/message")
async def receive_custom_message(request: Request):
    message = await request.json()
    response = await process_custom_message(message)
    return response