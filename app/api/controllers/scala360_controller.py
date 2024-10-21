from app.api.adapters.adapter_factory import get_adapter
from app.api.services.message_transformer import transform_message, transform_to_platform
from app.api.services.conversation_service import save_message_in_conversation
from tasks import process_message_task
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from app.api.models.message_model import MessageModel
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


async def process_scala360_message(full_message: dict) -> JSONResponse:
    """Process a message from Scala 360.""" 
    try:
        transformed_message = transform_message(full_message, "scala360")
        # Manage the conversation in Redis
        message_id = save_message_in_conversation(transformed_message)
        # Add the message_id to the transformed_message if needed
        transformed_message.message_id = message_id
        # Send the transformed_message directly to celery
        process_message_task(transformed_message)
        #nextStateId = result.get('nextStateId')
        #TODO: Remove this hardcoded nextStateId
        nextStateId = "36772604"
        return JSONResponse(content={"nextStateId": nextStateId}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


def process_return_message(messages: List, transformed_message: MessageModel):
    """Process a return message from Scala 360."""
    try:
        for message in messages:
            result = sendMessage(message, transformed_message)
            return result
    except Exception as e:
        print(f"Error in process_return_message: {str(e)}")
     


def sendMessage(message: Dict[str, Any], transformed_message: MessageModel):
    
    headers_send = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': transformed_message.metadata.required_fields.get('scala_auth')
    }
    
    url = f"https://app.scala360.com/webhook/{transformed_message.metadata.required_fields.get('slug')}/external/{transformed_message.metadata.required_fields.get('conversation-token')}"
    content = fix_message_content(message)
    data = {
        "messages": [{
            "content": content
        }]
    }
    
    response = requests.post(url, headers=headers_send, data=json.dumps(data))

    return response


def fix_message_content(message: Dict[str, Any]):
    """Fix the message content to be sent to Scala 360."""
    if message.get('text'):
        content = {
            "type": "text",
            "text": message['text']['body']
        }
    # TODO: Add the other types of messages
    return content