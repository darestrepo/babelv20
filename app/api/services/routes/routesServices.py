from fastapi import Request

async def requestFullMessageCreator(request: Request):
    """Create a full message from the request"""
    message = await request.json()
    headers = dict(request.headers)
    query_params = dict(request.query_params)

    full_message = {
        "message": message,
        "headers": headers,
        "query_params": query_params
    }

    return full_message