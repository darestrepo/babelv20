from api.services.message_transformer import transform_message
from api.services.message_dispatcher import dispatch_message

async def process_scala360_message(message: dict, headers: dict, query_params: dict):
    # Extract relevant information from headers and query_params
    relevant_headers = {
        "conversation_token": headers.get("conversation-token"),
        "unique_identifier": headers.get("unique-identifier")
    }
    relevant_query_params = {
        "default_box": query_params.get("default_box"),
        "auth": query_params.get("auth"),
        "slug": query_params.get("slug"),
        "whatsapp_number": query_params.get("whatsapp_number"),
        "teams_number": query_params.get("teams_number")
    }
    
    # Combine all data into a single dictionary
    full_message = {
        "message": message,
        "headers": relevant_headers,
        "query_params": relevant_query_params
    }
    standardized_message = transform_message(full_message, platform="scala360")
    dispatch_message(standardized_message)
    return {"status": "Message received and is being processed."}
