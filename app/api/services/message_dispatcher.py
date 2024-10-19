from celery_worker.tasks import process_message_task
from api.services.configuration_service import get_tenant_config, get_conversation_config
from utils.helpers import send_outbound_message

def dispatch_message(standardized_message: dict):
    platform = standardized_message['platform']
    tenant_id = standardized_message['metadata'].get('tenant_id')
    user_id = standardized_message['sender_id']

    tenant_config = get_tenant_config(tenant_id, platform)
    conversation_config = get_conversation_config(tenant_id, platform, user_id)

    if not tenant_config:
        raise ValueError(f"Configuration not found for tenant {tenant_id} and platform {platform}")

    # Merge tenant and conversation configs, with conversation config taking precedence
    config = {**tenant_config, **(conversation_config or {})}

    send_outbound_message(standardized_message, config)
