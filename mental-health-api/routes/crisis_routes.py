#mental-health-api/routes/crisis_routes.py
from flask import Blueprint, request, jsonify

crisis_blueprint = Blueprint('crisis', __name__)

@crisis_blueprint.route('/crisis/help', methods=['POST'])
def trigger_crisis_help():
    data = request.get_json()
    user_id = data.get('user_id')  # assuming crisis help will receive user ID or details
    # Implement notification to crisis team here (e.g., email, SMS, etc.)
    return jsonify({'message': 'Crisis help request has been sent'}), 200

@crisis_blueprint.route('/crisis/hotlines', methods=['GET'])
def get_hotlines():
    hotlines = [
        {'country': 'USA', 'hotline': '+1-800-273-8255'},
        {'country': 'UK', 'hotline': '+44 116 123'},
        # Add more hotlines or use dynamic data based on location.
    ]
    return jsonify({'hotlines': hotlines}), 200