from flask import Blueprint, jsonify
from app.utils.db import get_supabase

charities_bp = Blueprint('charities', __name__, url_prefix='/api/charities')
supabase = get_supabase()

@charities_bp.route('/', methods=['GET'])
def get_charities():
    try:
        charities = supabase.table('charities').select('*').execute()
        return jsonify({'charities': charities.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@charities_bp.route('/featured', methods=['GET'])
def get_featured_charities():
    try:
        charities = supabase.table('charities').select('*').eq('featured', True).limit(3).execute()
        return jsonify({'charities': charities.data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@charities_bp.route('/<charity_id>', methods=['GET'])
def get_charity(charity_id):
    try:
        charity = supabase.table('charities').select('*').eq('id', charity_id).execute()
        if not charity.data:
            return jsonify({'error': 'Charity not found'}), 404
        return jsonify({'charity': charity.data[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
