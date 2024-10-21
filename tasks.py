from celery import Celery
from celery.result import AsyncResult
from app.api.models.message_model import MessageModel
from app.api.services.redis.redis_service import get_message_by_id, get_last_message_from_conversation
from app.api.controllers.controller_factory import get_controller
import os
import json
from dotenv import load_dotenv
import redis

load_dotenv()

app_secret = os.getenv('APP_SECRET')
secret = json.loads(app_secret)
broker_url = f"redis://{secret['REDIS_BROKER_HOST']}:{secret['REDIS_BROKER_PORT']}/{secret['REDIS_BROKER_DB']}"
result_backend = f"redis://{secret['REDIS_BROKER_HOST']}:{secret['REDIS_BROKER_PORT']}/{secret['REDIS_BROKER_DB']}"
print(f"Broker URL: {broker_url}")
print(f"Result backend: {result_backend}")
celery_app = Celery('tasks', broker=broker_url, backend=result_backend)


# Define separate queues
celery_app.conf.task_routes = {
    'tasks.process_message': 'process_messages_queue',
}


def process_message_task(transformed_message: MessageModel, countdown: int = 0, sync: bool = False) -> str:
    """
    Process the transformed message and send it to the broker.

    Args:
        transformed_message (MessageModel): The transformed message to be processed.
        countdown (int): The number of seconds to wait before processing the message.
        sync (bool): Whether to wait for the result of the task execution.

    Returns:
        str: The result of the task execution.
    """
    message_id = transformed_message.message_id
    chat_conversation_id = transformed_message.chat_conversation_id
    print(f"Processing message with message_id: {message_id} and chat_conversation_id: {chat_conversation_id}")
    result = celery_app.send_task('tasks.process_message', 
                                  args=[message_id, chat_conversation_id], 
                                  countdown=countdown)

    if sync:
        actual_result = result.get()
        return actual_result
    else:
        return


@celery_app.task(queue='return_messages_queue')
def send_return_messages (chat_conversation_id, messages, message_id=None):
    """
    Send return messages to the appropriate controller.
    """
    if message_id:
        transformed_message = get_message_by_id (chat_conversation_id, message_id)            
    else:
        transformed_message = get_last_message_from_conversation(chat_conversation_id)

    if transformed_message:
            platform = transformed_message.platform
            function = get_controller(platform)
            function(messages, transformed_message)


