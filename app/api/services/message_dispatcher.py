from celery_worker.tasks import process_message_task

def dispatch_message(standardized_message: dict):
    process_message_task.delay(standardized_message)