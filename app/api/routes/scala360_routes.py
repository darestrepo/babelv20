from fastapi import APIRouter, Request
from api.controllers.scala360_controller import process_scala360_message

router = APIRouter()

@router.post("/message")
async def receive_scala360_message(request: Request):
    message = await request.json()
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    response = await process_scala360_message(message, headers, query_params)
    return response
