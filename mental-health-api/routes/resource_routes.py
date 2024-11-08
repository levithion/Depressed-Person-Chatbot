#mental-health-api/routes/resource_routes.py
from flask import Blueprint, jsonify
from models import Resource, db

resource_blueprint = Blueprint('resources', __name__)

@resource_blueprint.route('/resources', methods=['GET'])
def get_all_resources():
    resources = Resource.query.all()
    resources_data = [{'id': r.id, 'title': r.title, 'content': r.content} for r in resources]
    return jsonify({'resources': resources_data}), 200

@resource_blueprint.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    resource_data = {'id': resource.id, 'title': resource.title, 'content': resource.content}
    return jsonify(resource_data), 200
