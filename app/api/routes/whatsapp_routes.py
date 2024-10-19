from fastapi import APIRouter, Request
from api.controllers.whatsapp_controller import process_whatsapp_message

router = APIRouter()

@router.post("/message")
async def receive_whatsapp_message(request: Request):
    message = await request.json()
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    response = await process_whatsapp_message(message, headers, query_params)
    return response
