import json
import logging
import os
from typing import Optional

import stripe

from .event import Event, EventType
from .handlers import handlers

stripe.set_app_info('allwell-stripe', version='0.0.1')
stripe.api_version = '2020-08-27'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class StripeAPI:
    def __init__(self, webhook_secret: str = None) -> None:
        self.webhook_secret = webhook_secret
        self.errors = []
        self.webhook_handlers = handlers

    def create_payment_intent(self, amount=1999, currency='EUR',
                              automatic_payment_methods=True,
                              metadata=None) -> Optional[str]:
        if metadata is None:
            metadata = {}
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                automatic_payment_methods={
                    'enabled': automatic_payment_methods,
                },
                metadata=metadata
            )
            return intent.client_secret
        except stripe.error.StripeError as e:
            return self.errors.append(f'Stripe error: {str(e)}')
        except Exception as e:
            return self.errors.append(f'Unknown error: {str(e)}')

    def create_event(self, req_payload: bytes, req_signature: str) \
            -> Optional[Event]:

        if self.webhook_secret and req_signature:
            try:
                stripe_event = stripe.Webhook.construct_event(
                    payload=req_payload,
                    sig_header=req_signature,
                    secret=self.webhook_secret)
                return Event(data=stripe_event['data'],
                             event_type=stripe_event['type'])
            except (Exception,):
                error = 'Underlying stripe.Webhook.construct_event() ' \
                        'was unable to construct the event.'
                logger.exception(error)
                self.errors.append(error)
                return None
        else:
            request_data = json.loads(req_payload)
            return Event(data=request_data['data'],
                         event_type=request_data['type'])

    def webhook_handler(self, req_payload: bytes, req_signature: str) -> None:
        logger.debug('Handling Stripe Webhook request with payload')
        webhook_event = self.create_event(req_payload, req_signature)
        if not webhook_event:
            logger.debug(f'No Stripe Webhook Event created for payload {req_payload}')
            return
        else:
            if webhook_event.event_type not in self.webhook_handlers.keys():
                self.webhook_handlers[EventType.UNKNOWN_EVENT](webhook_event)
            else:
                self.webhook_handlers[webhook_event.event_type](webhook_event)
