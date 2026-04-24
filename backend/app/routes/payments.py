from flask import Blueprint, request, jsonify
from app.utils.db import get_supabase
from app.utils.decorators import token_required

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')
supabase = get_supabase()

@payments_bp.route('/subscribe', methods=['POST'])
@token_required
def subscribe(user_id):
    data = request.get_json()
    plan = data.get('plan', 'monthly')
    charity_id = data.get('charity_id')
    charity_percentage = data.get('charity_percentage', 10)
    try:
        supabase.table('users').update({
            'subscription_status': 'active', 'subscription_plan': plan,
            'charity_id': charity_id, 'charity_contribution_percentage': charity_percentage
        }).eq('id', user_id).execute()
        return jsonify({'message': 'Subscription created', 'plan': plan}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    return jsonify({'received': True}), 200
