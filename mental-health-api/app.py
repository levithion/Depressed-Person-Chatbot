import logging
from flask import Flask, jsonify, request
from extensions import db
from routes.user_routes import user_blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from routes.crisis_routes import crisis_blueprint
import ollama
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing
import os

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Database and JWT Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix='/')

# User model (For registration and login purposes)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Database Initialization (if not exists)
if not os.path.exists('mental_health.db'):
    with app.app_context():
        db.create_all()

# Error Handler
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find user by username
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

# Registration Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logging.error('Missing username or password')
        return jsonify({"msg": "Username and password are required"}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        logging.error(f"Username {username} already exists")
        return jsonify({"msg": "Username already exists"}), 400

    try:
        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)

        # Save the user in the database
        db.session.add(new_user)
        db.session.commit()  # Ensure the changes are committed to the database

        logging.info(f"User {username} registered successfully")
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        logging.error(f"Error during registration: {str(e)}")
        db.session.rollback()  # Rollback the transaction in case of an error
        return jsonify({"msg": "Internal Server Error"}), 500

# Ollama Response Generator
def generate_ollama_response(prompt):
    model = "llama3.2"  # Specify the model version
    response = ollama.generate(prompt=prompt, model=model)  # Add model argument
    if 'response' in response:
        return response['response']
    else:
        return "An error occurred while generating the response."

# Chatbot Endpoint
@app.route('/generate_response', methods=['POST'])
@jwt_required()
def generate_response():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    response = generate_ollama_response(prompt)
    return jsonify({'response': response})

# Run the app
if __name__ == '__main__':
    app.run(port=8877)