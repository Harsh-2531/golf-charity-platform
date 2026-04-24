from flask import Blueprint, request, jsonify
from app.utils.db import get_supabase
from app.utils.decorators import token_required
import stripe
import os

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')
supabase = get_supabase()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

PLANS = {
    'monthly': {'amount': 999,  'interval': 'month', 'name': 'Monthly Plan'},
    'yearly':  {'amount': 9999, 'interval': 'year',  'name': 'Yearly Plan'},
}

@payments_bp.route('/create-checkout', methods=['POST'])
@token_required
def create_checkout(user_id):
    data = request.get_json()
    plan = data.get('plan', 'monthly')
    charity_id = data.get('charity_id')
    charity_percentage = data.get('charity_percentage', 10)

    if plan not in PLANS:
        return jsonify({'error': 'Invalid plan'}), 400

    try:
        user = supabase.table('users').select('*').eq('id', user_id).execute()
        if not user.data:
            return jsonify({'error': 'User not found'}), 404
        user_data = user.data[0]

        customer_id = user_data.get('stripe_customer_id')
        if not customer_id:
            customer = stripe.Customer.create(
                email=user_data['email'],
                name=user_data.get('full_name', ''),
                metadata={'user_id': user_id}
            )
            customer_id = customer.id
            supabase.table('users').update({
                'stripe_customer_id': customer_id
            }).eq('id', user_id).execute()

        plan_info = PLANS[plan]
        price = stripe.Price.create(
            unit_amount=plan_info['amount'],
            currency='gbp',
            recurring={'interval': plan_info['interval']},
            product_data={'name': plan_info['name']},
        )

        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5500')
        checkout = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{'price': price.id, 'quantity': 1}],
            mode='subscription',
            success_url=f'{frontend_url}/dashboard.html?subscribed=true',
            cancel_url=f'{frontend_url}/subscription.html?cancelled=true',
            metadata={
                'user_id': user_id,
                'charity_id': charity_id or '',
                'charity_percentage': str(charity_percentage),
                'plan': plan
            }
        )

        return jsonify({'checkout_url': checkout.url, 'session_id': checkout.id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')

    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            event = stripe.Event.construct_from(request.get_json(), stripe.api_key)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            meta = session.get('metadata', {})
            user_id = meta.get('user_id')
            plan = meta.get('plan', 'monthly')
            charity_id = meta.get('charity_id') or None
            charity_pct = int(meta.get('charity_percentage', 10))

            if user_id:
                supabase.table('users').update({
                    'subscription_status': 'active',
                    'subscription_plan': plan,
                    'charity_id': charity_id,
                    'charity_contribution_percentage': charity_pct,
                }).eq('id', user_id).execute()

        elif event['type'] == 'customer.subscription.deleted':
            session = event['data']['object']
            customer_id = session.get('customer')
            user = supabase.table('users').select('id').eq('stripe_customer_id', customer_id).execute()
            if user.data:
                supabase.table('users').update({
                    'subscription_status': 'inactive'
                }).eq('id', user.data[0]['id']).execute()

        return jsonify({'received': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payments_bp.route('/status', methods=['GET'])
@token_required
def subscription_status(user_id):
    try:
        user = supabase.table('users').select(
            'subscription_status, subscription_plan, charity_id, charity_contribution_percentage'
        ).eq('id', user_id).execute()
        if not user.data:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.data[0]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payments_bp.route('/cancel', methods=['POST'])
@token_required
def cancel_subscription(user_id):
    try:
        user = supabase.table('users').select('stripe_customer_id').eq('id', user_id).execute()
        if not user.data or not user.data[0].get('stripe_customer_id'):
            return jsonify({'error': 'No active subscription'}), 404

        subscriptions = stripe.Subscription.list(customer=user.data[0]['stripe_customer_id'])
        for sub in subscriptions.auto_paging_iter():
            stripe.Subscription.cancel(sub.id)

        supabase.table('users').update({
            'subscription_status': 'inactive'
        }).eq('id', user_id).execute()

        return jsonify({'message': 'Subscription cancelled'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
