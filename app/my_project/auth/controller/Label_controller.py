from flask import jsonify, request
from ..dao.Label_dao import (
    create_label,
    get_label_by_id,
    get_all_labels as dao_get_all_labels,
    update_label,
    delete_label
)

def get_all_labels():
    """Retrieve all labels."""
    labels = dao_get_all_labels()
    labels_data = [{'id': label.id, 'name': label.name, 'country': label.country} for label in labels]
    return jsonify(labels_data)

def get_label(label_id):
    """Retrieve a label by its ID."""
    label = get_label_by_id(label_id)
    if label:
        label_data = {'id': label.id, 'name': label.name, 'country': label.country}
        return jsonify(label_data)
    return jsonify({'error': 'Label not found'}), 404

def add_label():
    """Add a new label."""
    data = request.get_json()
    name = data.get('name')
    country = data.get('country')

    if not name or not country:
        return jsonify({'error': 'name and country are required'}), 400

    label = create_label(name, country)
    return jsonify({
        'message': 'Label created successfully',
        'id': label.id,
        'name': label.name,
        'country': label.country
    }), 201

def update_label(label_id):
    """Update an existing label."""
    data = request.get_json()
    name = data.get('name')
    country = data.get('country')

    label = update_label(label_id, name, country)
    if label:
        return jsonify({'message': 'Label updated successfully', 'id': label.id})
    return jsonify({'error': 'Label not found'}), 404

def delete_label(label_id):
    """Delete a label by its ID."""
    success = delete_label(label_id)
    if success:
        return jsonify({'message': 'Label deleted successfully'})
    return jsonify({'error': 'Label not found'}), 404
