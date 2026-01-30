from contextvars import ContextVar
from enum import Enum
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class Role(Enum):
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"

# ContextVar to store the role of the current request
api_key_role: ContextVar[Role] = ContextVar("api_key_role")

def require_write_access(f):
    """Decorator to ensure the current API key has read-write access."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        role = api_key_role.get(None)
        if role != Role.READ_WRITE:
            logger.warning(f"Unauthorized write attempt to tool: {f.__name__}. Role: {role}")
            raise PermissionError(f"Tool '{f.__name__}' requires read-write access. Your current API key only has {role.value if role else 'no'} access.")
        return f(*args, **kwargs)
    return wrapper
