from enum import Enum


class EventType(Enum):
    PAYMENT_INTENT_SUCCEEDED = 'payment_intent.succeeded'
    PAYMENT_INTENT_FAILED = 'payment_intent.payment_failed'
    PAYMENT_INTENT_CREATED = 'payment_intent.created'
    CUSTOMER_SUBSCRIPTION_CREATED = 'customer.subscription.created'
    CUSTOMER_SUBSCRIPTION_UPDATED = 'customer.subscription.updated'
    CUSTOMER_SUBSCRIPTION_DELETED = 'customer.subscription.deleted'
    UNKNOWN_EVENT = 'unknown'


class Event:
    def __init__(self, data: dict, event_type: str) -> None:
        self.data = data
        self.event_type = EventType(event_type)
