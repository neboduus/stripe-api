import logging

from .event import EventType, Event

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def handle_unknown_webhook_event(webhook_event: Event) -> None:
    logger.debug(f'Received Stripe webhook event with unknown type!')


def handle_payment_intent_success(webhook_event: Event) -> None:
    logger.debug(f'💰 Payment received!')


def handle_payment_intent_failure(webhook_event: Event) -> None:
    logger.debug(f'❌ Payment failed')


def handle_payment_intent_created(webhook_event: Event) -> None:
    logger.debug(f'✓ Payment created')


handlers = {
    EventType.PAYMENT_INTENT_SUCCEEDED: handle_payment_intent_success,
    EventType.PAYMENT_INTENT_FAILED: handle_payment_intent_failure,
    EventType.PAYMENT_INTENT_CREATED: handle_payment_intent_created,
    EventType.UNKNOWN_EVENT: handle_unknown_webhook_event()
}
