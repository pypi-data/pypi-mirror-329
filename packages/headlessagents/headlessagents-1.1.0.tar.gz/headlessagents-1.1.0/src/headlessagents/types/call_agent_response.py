# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["CallAgentResponse"]


class CallAgentResponse(BaseModel):
    agent_id: str
    """ID of the agent that was called"""

    conversation_id: str
    """Identifier for the conversation"""

    function_result: Optional[Dict[str, object]] = None
    """Optional structured data returned by the agent, null if no structured data"""

    response: str
    """The agent's response text"""

    success: bool
    """Whether the call was successful"""

    thread_id: str
    """Unique identifier for this interaction thread"""
