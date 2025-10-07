from flask import jsonify, request
from flasgger import swag_from
from ..dao.Label_dao import (
    create_label,
    get_label_by_id,
    get_all_labels as dao_get_all_labels,
    update_label as dao_update_label,
    delete_label as dao_delete_label,
    insert_label_in_dao
)

# CREATE
@swag_from({
    'tags': ['Labels'],
    'description': 'Create a new label',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'country': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Label created successfully'}
    }
})
def create_label_route():
    data = request.get_json()
    label = create_label(data['name'], data['country'])
    labels_data = [{'id': label.id, 'name': label.name, 'country': label.country} for label in labels]
    return jsonify(labels_data)

def serialize_label(label):
    """Helper function to serialize a label entry."""
    return {
        'id': label.id,
        'name': label.name,
        'country': label.country
    }

# GET ALL
@swag_from({
    'tags': ['Labels'],
    'description': 'Get all labels',
    'responses': {
        200: {'description': 'A list of labels'}
    }
})

def get_all_labels():
    """Retrieve all labels."""
    labels = dao_get_all_labels()
    labels_data = [{'id': label.id, 'name': label.name, 'country': label.country} for label in labels]
    return jsonify(labels_data)

# GET ONE
@swag_from({
    'tags': ['Labels'],
    'description': 'Get label by ID',
    'parameters': [
        {'name': 'label_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Label found'},
        404: {'description': 'Label not found'}
    }
})

def get_label(label_id):
    """Retrieve a label by its ID."""
    label = get_label_by_id(label_id)
    if label:
        label_data = {'id': label.id, 'name': label.name, 'country': label.country}
        return jsonify(label_data)
    return jsonify({'error': 'Label not found'}), 404

@swag_from({
    'tags': ['Labels'],
    'description': 'Add a new label',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'country': {'type': 'string'}
                },
                'required': ['name', 'country']
            }
        }
    ],
    'responses': {
        201: {'description': 'Label created successfully'},
        400: {'description': 'Invalid input'}
    }
})

def add_label():
    """Add a new label."""
    data = request.get_json()
    name = data.get('name')
    country = data.get('country')

    if not name or not country:
        return jsonify({'error': 'name and country are required'}), 400

    result = insert_label_in_dao(name, country)

    if "error" in result:
        return jsonify(result), 500
    else:
        return jsonify(result), 201

# UPDATE
@swag_from({
    'tags': ['Labels'],
    'description': 'Update an existing label',
    'parameters': [
        {'name': 'label_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'required': True,
         'schema': {'properties': {
             'name': {'type': 'string'},
             'country': {'type': 'string'}
         }}}
    ],
    'responses': {
        200: {'description': 'Label updated successfully'},
        404: {'description': 'Label not found'}
    }
})

def update_label(label_id):
    """Update an existing label."""
    data = request.get_json()
    name = data.get('name')
    country = data.get('country')

    label = dao_update_label(label_id, name, country)
    if label:
        return jsonify({'message': 'Label updated successfully', 'id': label.id})
    return jsonify({'error': 'Label not found'}), 404

# DELETE
@swag_from({
    'tags': ['Labels'],
    'description': 'Delete label by ID',
    'parameters': [
        {'name': 'label_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Label deleted successfully'},
        404: {'description': 'Label not found'}
    }
})

def delete_label(label_id):
    """Delete a label by its ID."""
    success = dao_delete_label(label_id)
    if success:
        return jsonify({'message': 'Label deleted successfully'})
    return jsonify({'error': 'Label not found'}), 404
