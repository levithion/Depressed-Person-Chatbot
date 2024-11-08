from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import User, db

user_blueprint = Blueprint('user', __name__)

# User registration route
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    try:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"msg": "An error occurred during registration"}), 500

# User login route
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=username)
        return jsonify(access_token=token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

# Protected route for testing JWT
@user_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"msg": "Access granted to protected route."}), 200