from contextvars import ContextVar
from typing import Any, Dict

log_ctxvar: ContextVar[Dict[str, Any]] = ContextVar("LOG")
