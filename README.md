# Library to accept a payment through Stripe

> Based on [Accept a Payment Stripe Sample](https://github.com/stripe-samples/accept-a-payment) 

The core of the library resides in `/src`. The other 2 folders contain the 
following: 

- `flask_server`: A Flask server that exploits this library to accept a payment
- `html-client`: A HTML & Javascript app that shows how to interact with the 
  server in order to perform a payment

### How to use Stripe API?

In order to use the Stripe API you need to perform the following steps:

1. Include the `third_party_api/stripe_api` package in your application.

2. Use the `stripe_api.create_payment_intent()` method whenever you need to
   initialize a new payment as described by the demo Flask Server implemented
   at `third_party_api/stripe_api/flask_server/server.py`

3. Your Frontend Client will need to initialize the payment-

  - Basically we need our Frontend client to perform some specific actions
    so that Stripe is able to trust our Backend server.
  - Have a look at the HTML / JS / CSS client implemented within
    `third_party_api/stripe_api/html_client`

4. In order to handle the Stripe Webhook Events that your application needs you have to
   check the `EventType`s currently handled by this API in `third_party_api/stripe_api/lib/event.py`
   and adjust accordingly.

   In our case we handle only `payment_intent.succeeded`, `payment_intent.payment_failed`
   and `payment_intent.created` therefore the `EventType` class looks like this:

   ```python
   class EventType(Enum):
       PAYMENT_INTENT_SUCCEEDED = 'payment_intent.succeeded'
       PAYMENT_INTENT_FAILED = 'payment_intent.payment_failed'
       PAYMENT_INTENT_CREATED = 'payment_intent.created'
   ```

   If you want to handle a new event type just add a new event to this class, for example:

   ```python
   class EventType(Enum):
      ...
      PAYMENT_INTENT_CANCELED = 'payment_intent.canceled'
   ```

5. Once you decided you want to handle a new event type you have to
   check current event handlers in `third_party_api/stripe_api/lib/handlers.py`
   and adjust accordingly.

   Currently, the package contains handlers only for `payment_intent.succeeded`,
   `payment_intent.payment_failed` and `payment_intent.created` event types.

   If you want to add a new handler for a new event type, you just need to add a
   new handling function like this:

   ```python
   def handle_payment_intent_canceled(webhook_event: Event) -> None:
      logger.debug(f'Payment canceled')   
   ```

   And then plug it into the handlers list by associating it with the correct event type:

   ```python
   handlers = {
      ...
      EventType.PAYMENT_INTENT_CANCELED: handle_payment_intent_canceled
   }
   ```

6. After this configuration, you can use the Stripe API as used by the
   demo Flask Server implemented at `third_party_api/stripe_api/flask_server/server.py`

# How to Test Stripe API?

Testing the Stripe API is a bit more complex, it requires a full stack app
composed by a client and a server in order to emulate the entire payment cycle.

1. Create a webhook using your Stripe account in Test Mode by visiting your
   `Stripe Dashboard > Developers > Webhooks` and adding a new webhook with a
   domain. The domain can be invalid, because we will only use it to forward the
   events to the local machine.

   > Be careful that Stripe automatically deletes webhooks that have an invalid
   domain, therefore you may need to recreate the webhook once in a while

2. Install Stripe CLI and login by following the [following guide](https://stripe.com/docs/stripe-cli)

3. Forward the Stripe Webhook Events to your local machine, but select only the 
   events your webhook is able to handle.

   > Be careful on how you define your webhook domain and how you forward to
   your local server. If your webhook domain is `https://mytest.ai/webhook`
   and your local server listens at `/webhook` then your Stripe CLI command
   should be:

    ```shell
    stripe listen --events payment_intent.created,payment_intent.succeeded,payment_intent.failure --load-from-webhooks-api --forward-to 127.0.0.1:4242
    ```

   > Note that Stripe CLI will add the missing `/webhook` to the URL for you

   You should see something like:

    ```shell
     Your webhook signing secret is whsec_8d5d945c60834df9 (^C to quit)
    ```

4. Copy the webhook signing secret (`whsec_8d5d945c60834df9` in the example
   above) returned by the Stripe CLI in your environment (or `.env` file)
   by setting the `STRIPE_WEBHOOK_SECRET` variable.

5. Run the Flask server (assuming you are in the project root folder)

    ```
    export FLASK_APP=third_party_api/stripe_api/flask_server/server.py
    python3 -m flask run --port=4242
    ```

6. Visit `http://127.0.0.1:4242/` in your browser and perform a payment demo.

  - Use the following payment details to test a successful payment.

   ```
   Card number: 4242 4242 4242 4242
   Expiration: 04 / 24
   CVV: 242
   ```

  - change the Card number to `4000 0027 6000 3184` in order to test a card
    with 3D Secure enabled.

  - change the Card number to `4000 0000 0000 0002` in order to test a card that
    will end up with a Declined Payment.
  
