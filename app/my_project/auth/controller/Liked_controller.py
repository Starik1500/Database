from flask import jsonify, request
from ..dao.Liked_dao import (
    insert_liked_in_dao,
    create_liked,
    get_liked_by_id,
    get_all_liked as dao_get_all_liked,
    update_liked as dao_update_liked,
    delete_liked as dao_delete_liked
)
from flasgger import swag_from

def serialize_liked(liked):
    """Helper function to serialize a liked entry."""
    return {
        'id': liked.id,
        'artist': liked.artist,
        'album': liked.album,
        'user_id': liked.user_id
    }

@swag_from({
    'tags': ['Liked'],
    'responses': {
        200: {
            'description': 'List of liked entries',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'artist': {'type': 'string'},
                        'album': {'type': 'string'},
                        'user_id': {'type': 'integer'}
                    }
                }
            }
        }
    }
})

def get_all_liked():
    """Retrieve all liked entries."""
    liked_entries = dao_get_all_liked()
    liked_data = [
        {'id': liked.id, 'artist': liked.artist, 'album': liked.album, 'user_id': liked.user_id}
        for liked in liked_entries
    ]
    return jsonify(liked_data)

@swag_from({
    'tags': ['Liked'],
    'parameters': [
        {'name': 'liked_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {
            'description': 'Single liked entry',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'artist': {'type': 'string'},
                    'album': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                }
            }
        },
        404: {'description': 'Liked entry not found'}
    }
})

def get_liked(liked_id):
    """Retrieve a liked entry by its ID."""
    liked = get_liked_by_id(liked_id)
    if liked:
        liked_data = {'id': liked.id, 'artist': liked.artist, 'album': liked.album, 'user_id': liked.user_id}
        return jsonify(liked_data)
    return jsonify({'error': 'Liked entry not found'}), 404

@swag_from({
    'tags': ['Liked'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'artist': {'type': 'string'},
                    'album': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                },
                'required': ['artist', 'album', 'user_id']
            }
        }
    ],
    'responses': {
        201: {'description': 'Liked entry created successfully'},
        400: {'description': 'Missing parameters'},
        500: {'description': 'Internal server error'}
    }
})

def add_liked():
    """Add a new liked entry."""
    data = request.get_json()
    artist = data.get('artist')
    album = data.get('album')
    user_id = data.get('user_id')

    if not all([artist, album, user_id]):
        return jsonify({'error': 'artist, album, and user_id are required'}), 400

    result = insert_liked_in_dao(artist, album, user_id)

    if "error" in result:
        return jsonify(result), 500
    else:
        return jsonify(result), 201

@swag_from({
    'tags': ['Liked'],
    'parameters': [
        {'name': 'liked_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'artist': {'type': 'string'},
                    'album': {'type': 'string'},
                    'user_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Liked entry updated successfully'},
        404: {'description': 'Liked entry not found'}
    }
})

def update_liked(liked_id):
    """Update an existing liked entry."""
    data = request.get_json()
    artist = data.get('artist')
    album = data.get('album')
    user_id = data.get('user_id')

    liked = dao_update_liked(liked_id, artist, album, user_id)
    if liked:
        return jsonify({'message': 'Liked entry updated successfully', 'id': liked.id})
    return jsonify({'error': 'Liked entry not found'}), 404

@swag_from({
    'tags': ['Liked'],
    'parameters': [
        {'name': 'liked_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Liked entry deleted successfully'},
        404: {'description': 'Liked entry not found'}
    }
})

def delete_liked(liked_id):
    """Delete a liked entry by its ID."""
    success = dao_delete_liked(liked_id)
    if success:
        return jsonify({'message': 'Liked entry deleted successfully'})
    return jsonify({'error': 'Liked entry not found'}), 404
