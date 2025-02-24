# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ClientCallAgentParams"]


class ClientCallAgentParams(TypedDict, total=False):
    request: Required[str]
    """The prompt or request to send to the agent"""

    conversation_id: str
    """Optional conversation ID for continuing an existing conversation"""
