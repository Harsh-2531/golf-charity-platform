from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# CORS configuration
CORS(app,
     resources={
         r"/api/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": False
         }
     })

# Config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# Register blueprints
from app.routes.auth import auth_bp
from app.routes.users import users_bp
from app.routes.scores import scores_bp
from app.routes.charities import charities_bp
from app.routes.draws import draws_bp
from app.routes.payments import payments_bp
from app.routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(scores_bp)
app.register_blueprint(charities_bp)
app.register_blueprint(draws_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)