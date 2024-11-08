#mental-health-api/routes/routes/mood_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Mood, db
from datetime import date

mood_blueprint = Blueprint('mood', __name__)

@mood_blueprint.route('/mood', methods=['POST'])
@jwt_required()
def record_mood():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_mood = Mood(mood=data['mood'], date=date.today(), user_id=user_id)
    db.session.add(new_mood)
    db.session.commit()
    return jsonify({'message': 'Mood recorded successfully'}), 201

@mood_blueprint.route('/mood/history', methods=['GET'])
@jwt_required()
def get_mood_history():
    user_id = get_jwt_identity()
    mood_history = Mood.query.filter_by(user_id=user_id).all()
    history = [{'mood': m.mood, 'date': m.date.isoformat()} for m in mood_history]
    return jsonify({'mood_history': history}), 200
