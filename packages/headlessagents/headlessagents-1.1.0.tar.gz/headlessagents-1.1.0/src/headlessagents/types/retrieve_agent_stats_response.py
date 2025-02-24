# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = [
    "RetrieveAgentStatsResponse",
    "MessageDistribution",
    "MessageLength",
    "MessageLengthAssistant",
    "MessageLengthUser",
    "MessagesPerConversation",
    "ResponseTime",
    "TurnsPerConversation",
    "UsageTimeline",
]


class MessageDistribution(BaseModel):
    assistant_messages: Optional[int] = None

    sample_size: Optional[int] = None

    user_messages: Optional[int] = None


class MessageLengthAssistant(BaseModel):
    average: Optional[float] = None

    max: Optional[int] = None

    min: Optional[int] = None

    sample_size: Optional[int] = None


class MessageLengthUser(BaseModel):
    average: Optional[float] = None

    max: Optional[int] = None

    min: Optional[int] = None

    sample_size: Optional[int] = None


class MessageLength(BaseModel):
    assistant: Optional[MessageLengthAssistant] = None

    user: Optional[MessageLengthUser] = None


class MessagesPerConversation(BaseModel):
    average: Optional[float] = None

    max: Optional[int] = None

    min: Optional[int] = None


class ResponseTime(BaseModel):
    average_seconds: Optional[float] = None

    max_seconds: Optional[float] = None

    min_seconds: Optional[float] = None

    sample_size: Optional[int] = None


class TurnsPerConversation(BaseModel):
    average: Optional[float] = None

    sample_size: Optional[int] = None


class UsageTimeline(BaseModel):
    first_conversation: Optional[datetime] = None

    last_24h: Optional[int] = None

    last_30d: Optional[int] = None

    last_7d: Optional[int] = None

    last_conversation: Optional[datetime] = None


class RetrieveAgentStatsResponse(BaseModel):
    agent_id: str

    stats_generated_at: datetime

    message_distribution: Optional[MessageDistribution] = None

    message_length: Optional[MessageLength] = None

    messages_per_conversation: Optional[MessagesPerConversation] = None

    response_time: Optional[ResponseTime] = None

    total_conversations: Optional[int] = None

    total_messages: Optional[int] = None

    turns_per_conversation: Optional[TurnsPerConversation] = None

    usage_timeline: Optional[UsageTimeline] = None
