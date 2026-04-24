from flask import Blueprint, jsonify
from app.utils.db import get_supabase
from app.utils.decorators import token_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')
supabase = get_supabase()

@users_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    try:
        user = supabase.table('users').select('*').eq('id', user_id).execute()
        if not user.data:
            return jsonify({'error': 'User not found'}), 404
        user_data = user.data[0]
        user_data.pop('password', None)
        return jsonify({'user': user_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(user_id):
    try:
        user = supabase.table('users').select('*').eq('id', user_id).execute()
        if not user.data:
            return jsonify({'error': 'User not found'}), 404
        user_data = user.data[0]
        user_data.pop('password', None)
        scores = supabase.table('scores').select('*').eq('user_id', user_id).order('date', desc=True).limit(5).execute()
        return jsonify({
            'user': user_data,
            'latest_scores': scores.data,
            'total_winnings': 0,
            'paid_amount': 0,
            'pending_winnings': 0,
            'recent_wins': []
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
