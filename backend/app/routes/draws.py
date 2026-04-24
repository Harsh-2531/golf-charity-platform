from flask import Blueprint, request, jsonify
from app.utils.db import get_supabase
from datetime import datetime
import random
import uuid

draws_bp = Blueprint('draws', __name__, url_prefix='/api/draws')
supabase = get_supabase()

SUBSCRIPTION_PRICE = {'monthly': 9.99, 'yearly': 99.99}
PRIZE_SPLIT = {5: 0.40, 4: 0.35, 3: 0.25}
CHARITY_PERCENTAGE = 0.10


def calculate_prize_pool(month):
    users = supabase.table('users').select(
        'subscription_status, subscription_plan, charity_contribution_percentage'
    ).eq('subscription_status', 'active').execute()

    total_subscriptions = 0.0
    total_charity = 0.0

    for user in users.data:
        plan = user.get('subscription_plan', 'monthly')
        price = SUBSCRIPTION_PRICE.get(plan, 9.99)
        charity_pct = (user.get('charity_contribution_percentage') or 10) / 100
        total_subscriptions += price
        total_charity += price * charity_pct

    prize_pool = total_subscriptions - total_charity
    return round(prize_pool, 2), round(total_charity, 2)


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


def find_winners(winning_numbers, draw_id, prize_pool, jackpot_amount=0):
    users = supabase.table('users').select('*').eq('subscription_status', 'active').execute()

    winners = {5: [], 4: [], 3: []}

    for user in users.data:
        scores_data = supabase.table('scores').select('score') \
            .eq('user_id', user['id']).order('date', desc=True).limit(5).execute()
        user_scores = [s['score'] for s in scores_data.data]
        matches = len(set(user_scores) & set(winning_numbers))
        if matches in winners:
            winners[matches].append(user['id'])

    recorded = []
    has_5_match = len(winners[5]) > 0

    for match_type in [5, 4, 3]:
        if not winners[match_type]:
            continue

        if match_type == 5:
            pool = prize_pool * PRIZE_SPLIT[5] + jackpot_amount
        else:
            pool = prize_pool * PRIZE_SPLIT[match_type]

        prize_per_winner = round(pool / len(winners[match_type]), 2)

        for user_id in winners[match_type]:
            supabase.table('draw_winners').insert({
                'id': str(uuid.uuid4()),
                'draw_id': draw_id,
                'user_id': user_id,
                'match_type': match_type,
                'prize_amount': prize_per_winner,
                'verification_status': 'pending',
                'payment_status': 'pending'
            }).execute()
            recorded.append({
                'user_id': user_id,
                'match_type': match_type,
                'prize_amount': prize_per_winner
            })

    return recorded, has_5_match


@draws_bp.route('/simulate', methods=['POST'])
def simulate_draw():
    data = request.get_json()
    draw_type = data.get('algorithm', 'random')
    month = data.get('month', datetime.utcnow().strftime('%Y-%m'))

    try:
        winning_numbers = generate_draw_numbers(draw_type)
        prize_pool, charity_total = calculate_prize_pool(month)

        users = supabase.table('users').select('*').eq('subscription_status', 'active').execute()
        preview = {5: [], 4: [], 3: []}

        for user in users.data:
            scores_data = supabase.table('scores').select('score') \
                .eq('user_id', user['id']).order('date', desc=True).limit(5).execute()
            user_scores = [s['score'] for s in scores_data.data]
            matches = len(set(user_scores) & set(winning_numbers))
            if matches in preview:
                preview[matches].append({
                    'user_id': user['id'],
                    'email': user['email'],
                    'scores': user_scores
                })

        existing_draw = supabase.table('draws').select('jackpot_amount') \
            .eq('jackpot_rolled_over', True).order('created_at', desc=True).limit(1).execute()
        jackpot = existing_draw.data[0]['jackpot_amount'] if existing_draw.data else 0

        return jsonify({
            'winning_numbers': winning_numbers,
            'prize_pool': prize_pool,
            'charity_total': charity_total,
            'jackpot_carried_forward': jackpot,
            'prize_breakdown': {
                '5_match_pool': round(prize_pool * 0.40 + jackpot, 2),
                '4_match_pool': round(prize_pool * 0.35, 2),
                '3_match_pool': round(prize_pool * 0.25, 2),
            },
            'preview_winners': {
                '5_match': len(preview[5]),
                '4_match': len(preview[4]),
                '3_match': len(preview[3]),
            },
            'active_subscribers': len(users.data)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@draws_bp.route('/publish', methods=['POST'])
def publish_draw():
    data = request.get_json()
    draw_type = data.get('algorithm', 'random')
    month = data.get('month', datetime.utcnow().strftime('%Y-%m'))

    try:
        existing = supabase.table('draws').select('*').eq('month', month).execute()
        if existing.data:
            return jsonify({'error': 'Draw already exists for this month'}), 400

        winning_numbers = generate_draw_numbers(draw_type)
        prize_pool, charity_total = calculate_prize_pool(month)

        rolled = supabase.table('draws').select('jackpot_amount') \
            .eq('jackpot_rolled_over', True).order('created_at', desc=True).limit(1).execute()
        jackpot_amount = rolled.data[0]['jackpot_amount'] if rolled.data else 0

        draw = supabase.table('draws').insert({
            'id': str(uuid.uuid4()),
            'month': month,
            'draw_type': draw_type,
            'status': 'published',
            'winning_numbers': winning_numbers,
            'prize_pool_total': prize_pool,
            'jackpot_amount': jackpot_amount,
            'published_at': datetime.utcnow().isoformat()
        }).execute()

        draw_id = draw.data[0]['id']
        winners, has_5_match = find_winners(winning_numbers, draw_id, prize_pool, jackpot_amount)

        if not has_5_match:
            new_jackpot = round(prize_pool * 0.40 + jackpot_amount, 2)
            supabase.table('draws').update({
                'jackpot_rolled_over': True,
                'jackpot_amount': new_jackpot
            }).eq('id', draw_id).execute()

        return jsonify({
            'message': 'Draw published',
            'draw_id': draw_id,
            'winning_numbers': winning_numbers,
            'prize_pool': prize_pool,
            'charity_total': charity_total,
            'jackpot_rolled_over': not has_5_match,
            'winners_count': len(winners),
            'winners': winners
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@draws_bp.route('/history', methods=['GET'])
def draw_history():
    try:
        draws = supabase.table('draws').select('*').order('created_at', desc=True).execute()
        return jsonify({'draws': draws.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@draws_bp.route('/latest', methods=['GET'])
def latest_draw():
    try:
        draw = supabase.table('draws').select('*') \
            .eq('status', 'published').order('created_at', desc=True).limit(1).execute()
        if not draw.data:
            return jsonify({'draw': None}), 200
        return jsonify({'draw': draw.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
