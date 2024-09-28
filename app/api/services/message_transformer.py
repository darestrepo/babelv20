def transform_message(message: dict, platform: str) -> dict:
    # Transform the message based on the platform
    standardized = {
        "platform": platform,
        "user_id": message.get("user_id"),
        "content": message.get("content"),
        "timestamp": message.get("timestamp"),
    }
    return standardized

def transform_response(response: dict, platform: str) -> dict:
    # Transform the response based on the platform
    if platform == "whatsapp":
        return {
            "recipient_id": response.get("user_id"),
            "message": response.get("content"),
        }
    elif platform == "messenger":
        return {
            "recipient_id": response.get("user_id"),
            "message": response.get("content"),
        }
    elif platform == "telegram":
        return {
            "chat_id": response.get("user_id"),
            "text": response.get("content"),
        }
    elif platform == "instagram":
        return {
            "recipient_id": response.get("user_id"),
            "message": response.get("content"),
        }
    elif platform == "custom":
        return {
            "recipient_id": response.get("user_id"),
            "message": response.get("content"),
        }
    # Handle other platforms similarly
    return response