from flask import Blueprint, request, jsonify
from app.utils.db import get_supabase
from app.utils.decorators import token_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
supabase = get_supabase()

@admin_bp.route('/users', methods=['GET'])
@token_required
def get_all_users(user_id):
    try:
        users = supabase.table('users').select('*').execute()
        for user in users.data:
            user.pop('password', None)
        return jsonify({'users': users.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/winners', methods=['GET'])
@token_required
def get_all_winners(user_id):
    try:
        winners = supabase.table('draw_winners').select('*').execute()
        return jsonify({'winners': winners.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/winners/<winner_id>/verify', methods=['PUT'])
@token_required
def verify_winner(user_id, winner_id):
    data = request.get_json()
    status = data.get('status')
    try:
        supabase.table('draw_winners').update({
            'verification_status': status,
            'verified_at': datetime.utcnow().isoformat()
        }).eq('id', winner_id).execute()
        return jsonify({'message': f'Winner {status}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(user_id):
    try:
        users = supabase.table('users').select('*').execute()
        active_users = [u for u in users.data if u.get('subscription_status') == 'active']
        draws = supabase.table('draws').select('*').execute()
        return jsonify({
            'total_users': len(users.data),
            'active_subscriptions': len(active_users),
            'total_draws': len(draws.data)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
