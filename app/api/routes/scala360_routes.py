from fastapi import APIRouter, Request
from app.api.controllers.scala360_controller import process_scala360_message
from app.api.services.routes.routesServices import requestFullMessageCreator

router = APIRouter()


@router.post("/input")
async def receive_scala360_input(request: Request):
    """Receive a message from Scala 360 and redirect to /message endpoint."""
    return await receive_scala360_message(request)

@router.post("/message")
async def receive_scala360_message(request: Request):
    """Receive a message from Scala 360."""
    full_message = await requestFullMessageCreator(request) 
    response = await process_scala360_message(full_message)
    return response
