from flask import jsonify, request
from ..dao.Liked_dao import (
    create_liked,
    get_liked_by_id,
    get_all_liked as dao_get_all_liked,
    update_liked,
    delete_liked
)

def get_all_liked():
    """Retrieve all liked entries."""
    liked_entries = dao_get_all_liked()
    liked_data = [
        {'id': liked.id, 'artist': liked.artist, 'album': liked.album, 'user_id': liked.user_id}
        for liked in liked_entries
    ]
    return jsonify(liked_data)

def get_liked(liked_id):
    """Retrieve a liked entry by its ID."""
    liked = get_liked_by_id(liked_id)
    if liked:
        liked_data = {'id': liked.id, 'artist': liked.artist, 'album': liked.album, 'user_id': liked.user_id}
        return jsonify(liked_data)
    return jsonify({'error': 'Liked entry not found'}), 404

def add_liked():
    """Add a new liked entry."""
    data = request.get_json()
    artist = data.get('artist')
    album = data.get('album')
    user_id = data.get('user_id')

    if not all([artist, album, user_id]):
        return jsonify({'error': 'artist, album, and user_id are required'}), 400

    liked = create_liked(artist, album, user_id)
    return jsonify({
        'message': 'Liked entry created successfully',
        'id': liked.id,
        'artist': liked.artist,
        'album': liked.album,
        'user_id': liked.user_id
    }), 201

def update_liked(liked_id):
    """Update an existing liked entry."""
    data = request.get_json()
    artist = data.get('artist')
    album = data.get('album')
    user_id = data.get('user_id')

    liked = update_liked(liked_id, artist, album, user_id)
    if liked:
        return jsonify({'message': 'Liked entry updated successfully', 'id': liked.id})
    return jsonify({'error': 'Liked entry not found'}), 404

def delete_liked(liked_id):
    """Delete a liked entry by its ID."""
    success = delete_liked(liked_id)
    if success:
        return jsonify({'message': 'Liked entry deleted successfully'})
    return jsonify({'error': 'Liked entry not found'}), 404
