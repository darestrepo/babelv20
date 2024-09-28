from fastapi import APIRouter, Request
from api.controllers.instagram_controller import process_instagram_message

router = APIRouter()

@router.post("/instagram/message")
async def receive_instagram_message(request: Request):
    message = await request.json()
    response = await process_instagram_message(message)
    return response