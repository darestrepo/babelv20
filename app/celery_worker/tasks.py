from celery import Celery
from api.services.message_transformer import transform_response
from app.core.config import settings
from utils.helpers import send_response

celery_app = Celery(
    'celery_worker',
    broker=f'redis://{settings.REDIS_BROKER_HOST}:{settings.REDIS_BROKER_PORT}/{settings.REDIS_BROKER_DB}',
    backend=f'redis://{settings.REDIS_BROKER_HOST}:{settings.REDIS_BROKER_PORT}/{settings.REDIS_BROKER_DB}'
)

@celery_app.task
def process_message_task(standardized_message):
    # Process the message with an external application
    response = external_app_process(standardized_message)
    transformed_response = transform_response(response, standardized_message['platform'])
    send_response(transformed_response, standardized_message['platform'])

def external_app_process(message):
    # Placeholder for external processing logic
    response = {
        "user_id": message["sender_id"],
        "content": f"Processed: {message['content']}",
        "timestamp": message.get("timestamp"),
    }
    return response
