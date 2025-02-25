from typing import Optional
from chat.models import Message
from util import get_iso8601_timestamp, get_unix_timestamp

def create_message(role: str, content: str, reasoning_content: Optional[str] = None, provider: Optional[str] = None, model: Optional[str] = None, id: Optional[str] = None, reasoning_effort: Optional[float] = None) -> Message:
    """Create a Message object with optional fields.
    
    Args:
        role: Message role (user/assistant/system) 
        content: Message content
        reasoning_content: Optional reasoning content
        provider: Optional provider name
        model: Optional model name
        id: Optional message ID
        reasoning_effort: Optional reasoning effort value
        
    Returns:
        Message: Message object with role, content, and optional fields
    """
    message_data = {
        "role": role,
        "content": content,
        "timestamp": get_iso8601_timestamp(),
        "unix_timestamp": get_unix_timestamp()
    }

    if reasoning_content is not None:
        message_data["reasoning_content"] = reasoning_content

    if provider is not None:
        message_data["provider"] = provider

    if model is not None:
        message_data["model"] = model

    if id is not None:
        message_data["id"] = id

    if reasoning_effort is not None:
        message_data["reasoning_effort"] = reasoning_effort

    return Message.from_dict(message_data)
