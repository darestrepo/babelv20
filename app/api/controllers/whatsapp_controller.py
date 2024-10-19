from api.services.message_transformer import transform_message
from api.services.message_dispatcher import dispatch_message
from api.services.configuration_service import update_conversation_config

async def process_whatsapp_message(message: dict, headers: dict, query_params: dict):
    tenant_id = headers.get('X-Tenant-ID')  # Assume tenant ID is passed in headers
    full_message = {
        "message": message,
        "headers": headers,
        "query_params": query_params,
        "metadata": {"tenant_id": tenant_id}
    }
    standardized_message = transform_message(full_message, platform="whatsapp")
    
    # Update conversation config if necessary
    if 'conversation_id' in message:
        update_conversation_config(tenant_id, "whatsapp", message['from'], 
                                   {"conversation_id": message['conversation_id']})
    
    dispatch_message(standardized_message)
    return {"status": "Message received and is being processed."}
