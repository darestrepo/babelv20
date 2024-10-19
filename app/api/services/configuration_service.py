from typing import Optional, Dict, Any
from app.core.config import settings
import redis
import json

# Redis connection for database
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

def get_tenant_config(tenant_id: str, platform: str) -> Optional[Dict[str, Any]]:
    """Retrieve tenant-specific configuration from Redis."""
    key = f"channels_{tenant_id}"
    config = redis_client.hget(key, platform)
    return json.loads(config) if config else None

def get_conversation_config(tenant_id: str, platform: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve conversation-specific configuration from Redis."""
    key = f"channel_{tenant_id}_{user_id}"
    config = redis_client.hget(key, platform)
    return json.loads(config) if config else None

def set_tenant_config(tenant_id: str, platform: str, config: Dict[str, Any]):
    """Set tenant-specific configuration in Redis."""
    key = f"channels_{tenant_id}"
    redis_client.hset(key, platform, json.dumps(config))
    redis_client.expire(key, 604800)  # 1 week TTL

def set_conversation_config(tenant_id: str, platform: str, user_id: str, config: Dict[str, Any]):
    """Set conversation-specific configuration in Redis."""
    key = f"channel_{tenant_id}_{user_id}"
    redis_client.hset(key, platform, json.dumps(config))
    redis_client.expire(key, 172800)  # 2 days TTL

def update_conversation_config(tenant_id: str, platform: str, user_id: str, updates: Dict[str, Any]):
    """Update conversation-specific configuration in Redis."""
    current_config = get_conversation_config(tenant_id, platform, user_id) or {}
    current_config.update(updates)
    set_conversation_config(tenant_id, platform, user_id, current_config)
