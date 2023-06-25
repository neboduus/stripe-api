from enum import Enum


class EventType(Enum):
    PAYMENT_INTENT_SUCCEEDED = 'payment_intent.succeeded'
    PAYMENT_INTENT_FAILED = 'payment_intent.payment_failed'
    PAYMENT_INTENT_CREATED = 'payment_intent.created'
    UNKNOWN_EVENT = 'unknown'


class Event:
    def __init__(self, data: dict, event_type: str) -> None:
        self.data = data
        self.event_type = EventType(event_type)
