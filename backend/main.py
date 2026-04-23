from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Better CORS configuration
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

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    return jsonify({"message": "Signup successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)