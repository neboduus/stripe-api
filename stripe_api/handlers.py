import logging

from .event import EventType, Event

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def handle_unknown_webhook_event(webhook_event: Event) -> None:
    logger.debug('Received Stripe webhook event with unknown type!')


def handle_payment_intent_success(webhook_event: Event) -> None:
    logger.debug('💰 Payment received!')


def handle_payment_intent_failure(webhook_event: Event) -> None:
    logger.debug('❌ Payment failed')


def handle_payment_intent_created(webhook_event: Event) -> None:
    logger.debug('✓ Payment created')


def handle_customer_subscription_created(webhook_event: Event) -> None:
    logger.debug('✓ Customer subscription created')
    logger.debug(webhook_event.__dict__)


def handle_customer_subscription_updated(webhook_event: Event) -> None:
    logger.debug('✓ Customer subscription updated')
    logger.debug(webhook_event.__dict__)


def handle_customer_subscription_deleted(webhook_event: Event) -> None:
    logger.debug('❌ Customer subscription deleted')
    logger.debug(webhook_event.__dict__)


handlers = {
    EventType.PAYMENT_INTENT_SUCCEEDED: handle_payment_intent_success,
    EventType.PAYMENT_INTENT_FAILED: handle_payment_intent_failure,
    EventType.PAYMENT_INTENT_CREATED: handle_payment_intent_created,
    EventType.CUSTOMER_SUBSCRIPTION_CREATED:
        handle_customer_subscription_created,
    EventType.CUSTOMER_SUBSCRIPTION_UPDATED:
        handle_customer_subscription_created,
    EventType.CUSTOMER_SUBSCRIPTION_DELETED:
        handle_customer_subscription_deleted,
    EventType.UNKNOWN_EVENT: handle_unknown_webhook_event
}
