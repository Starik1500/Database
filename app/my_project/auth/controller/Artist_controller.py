from flask import jsonify, request
from ..dao.Artist_dao import get_all_artists, get_artist_by_id, create_artist, update_artist, delete_artist

def get_artists():
    artists = get_all_artists()
    artist_data = [
        {
            'id': artist.id,
            'name': artist.name,
            'in_playlist': artist.in_playlist,
            'genre': artist.genre,
            'label_id': artist.label_id
        } for artist in artists
    ]
    return jsonify(artist_data)

def get_artist(artist_id):
    artist = get_artist_by_id(artist_id)
    if artist:
        artist_data = {
            'id': artist.id,
            'name': artist.name,
            'in_playlist': artist.in_playlist,
            'genre': artist.genre,
            'label_id': artist.label_id
        }
        return jsonify(artist_data)
    return jsonify({'error': 'Artist not found'}), 404

def create_artist_route():
    data = request.get_json()
    new_artist = create_artist(data)
    return jsonify({'message': 'Artist created successfully', 'artist_id': new_artist.id}), 201

def update_artist_route(artist_id):
    data = request.get_json()
    artist = update_artist(artist_id, data)
    if artist:
        return jsonify({'message': 'Artist updated successfully'})
    return jsonify({'error': 'Artist not found'}), 404

def delete_artist_route(artist_id):
    artist = delete_artist(artist_id)
    if artist:
        return jsonify({'message': 'Artist deleted successfully'})
    return jsonify({'error': 'Artist not found'}), 404