import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, jsonify, request

from stripe_api.stripe_api import StripeAPI

load_dotenv(find_dotenv())
webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
static_dir = str(os.path.abspath(
    os.path.join(__file__, "../..", os.getenv("FLASK_STATIC_DIR"))))

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
