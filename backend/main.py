from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from app.routes.scores import scores_bp
from app.routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

app.register_blueprint(auth_bp)
app.register_blueprint(scores_bp)

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)