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
        # Remove sensitive fields
        user_data.pop('password', None)
        
        return jsonify({'user': user_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(user_id):
    try:
        # Get user
        user = supabase.table('users').select('*').eq('id', user_id).execute()
        user.data[0].pop('password', None)
        
        # Get latest 5 scores
        scores = supabase.table('golf_scores').select('*').eq('user_id', user_id).order('score_date', desc=True).limit(5).execute()
        
        # Get winnings
        winnings = supabase.table('draw_winners').select('*').eq('user_id', user_id).execute()
        
        total_won = sum([w['prize_amount'] for w in winnings.data if w['prize_amount']])
        paid_amount = sum([w['prize_amount'] for w in winnings.data if w['payment_status'] == 'paid' and w['prize_amount']])
        
        return jsonify({
            'user': user.data[0],
            'latest_scores': scores.data,
            'total_winnings': float(total_won),
            'paid_amount': float(paid_amount),
            'pending_winnings': float(total_won - paid_amount),
            'recent_wins': winnings.data[:5]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400