from flask import Blueprint, request, jsonify
from app.utils.db import get_supabase
from datetime import datetime
import random, uuid

draws_bp = Blueprint('draws', __name__, url_prefix='/api/draws')
supabase = get_supabase()

def generate_draw_numbers(algorithm='random'):
    if algorithm == 'random':
        return sorted(random.sample(range(1, 46), 5))
    try:
        scores_data = supabase.table('scores').select('score').execute()
        score_counts = {}
        for entry in scores_data.data:
            s = entry['score']
            score_counts[s] = score_counts.get(s, 0) + 1
        if score_counts:
            sorted_scores = sorted(score_counts.items(), key=lambda x: x[1], reverse=True)
            selected = list(set([score for score, _ in sorted_scores[:5]]))
            while len(selected) < 5:
                n = random.randint(1, 45)
                if n not in selected:
                    selected.append(n)
            return sorted(selected[:5])
    except:
        pass
    return sorted(random.sample(range(1, 46), 5))

@draws_bp.route('/simulate', methods=['POST'])
def simulate_draw():
    data = request.get_json()
    draw_type = data.get('algorithm', 'random')
    try:
        winning_numbers = generate_draw_numbers(draw_type)
        users = supabase.table('users').select('*').eq('subscription_status', 'active').execute()
        winners = []
        for user in users.data:
            scores_data = supabase.table('scores').select('score').eq('user_id', user['id']).order('date', desc=True).limit(5).execute()
            user_scores = [s['score'] for s in scores_data.data]
            matches = len(set(user_scores) & set(winning_numbers))
            if matches >= 3:
                winners.append({'user_id': user['id'], 'email': user['email'], 'match_type': matches})
        return jsonify({'winning_numbers': winning_numbers, 'winners_count': len(winners), 'sample_winners': winners[:5]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@draws_bp.route('/publish', methods=['POST'])
def publish_draw():
    data = request.get_json()
    draw_type = data.get('algorithm', 'random')
    month = data.get('month')
    try:
        existing = supabase.table('draws').select('*').eq('month', month).execute()
        if existing.data:
            return jsonify({'error': 'Draw already exists for this month'}), 400
        winning_numbers = generate_draw_numbers(draw_type)
        draw = supabase.table('draws').insert({
            'id': str(uuid.uuid4()), 'month': month, 'draw_type': draw_type,
            'status': 'published', 'winning_numbers': winning_numbers,
            'published_at': datetime.utcnow().isoformat()
        }).execute()
        return jsonify({'message': 'Draw published', 'draw_id': draw.data[0]['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
