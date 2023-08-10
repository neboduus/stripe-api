import os

import stripe
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, jsonify, request

from stripe_api.stripe_api import StripeAPI

load_dotenv(find_dotenv())
webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
price_id = os.getenv('STRIPE_AW_PRICE_ID')
bubble_successful_subs_page = os.getenv('SUCCESSFUL_SUBSCRIPTION_PAGE')
bubble_failed_subs_page = os.getenv('FAILED_SUBSCRIPTION_PAGE')
static_dir = str(os.path.abspath(
    os.path.join(__file__, "..", os.getenv("FLASK_STATIC_DIR"))))
stripe.api_key = os.getenv("STRIPE_API_KEY")


app = Flask(__name__,
            static_folder=static_dir,
            static_url_path="",
            template_folder=static_dir)


@app.route('/', methods=['GET'])
def get_root():
    return render_template('index.html')


@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')})


@app.route('/create-payment-intent', methods=['GET'])
def create_payment():
    stripe_api = StripeAPI(webhook_secret=webhook_secret)
    intent_client_secret = stripe_api.create_payment_intent()
    errors = ','.join(stripe_api.errors)
    if errors:
        return jsonify({'error': {'message': errors}}), 400
    return jsonify({'clientSecret': intent_client_secret})


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    req_data = request.json
    quantity = req_data['quantity']
    customer_email = req_data['customer_email']

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': quantity,
                },
            ],
            mode='subscription',
            success_url='https://web-app-aw.bubbleapps.io/version-571j'
                        '/stripe_success_page',
            cancel_url='https://web-app-aw.bubbleapps.io/version-571j'
                       '/stripe_success_page',
            metadata={'customer_email': customer_email}
        )
    except Exception as e:
        return str(e)

    return jsonify({'checkout_session_url': checkout_session.url,
                    'checkout_session_id': checkout_session.id}), 200


@app.route('/webhook', methods=['POST'])
def webhook_received():
    req_sign = request.headers.get('stripe-signature')
    req_data = request.data
    stripe_api = StripeAPI(webhook_secret=webhook_secret)
    stripe_api.webhook_handler(req_data, req_sign)
    errors = ','.join(stripe_api.errors)
    if errors:
        return jsonify({'error': {'message': errors}}), 400
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(port=4242, debug=True)
