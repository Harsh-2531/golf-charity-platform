from functools import wraps
from flask import request, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token required'}), 401
        try:
            token = token.split(' ')[1]
            decoded = jwt.decode(token, os.getenv('JWT_SECRET', 'secret'), algorithms=['HS256'])
            user_id = decoded['user_id']
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
        return f(user_id, *args, **kwargs)
    return decorated
