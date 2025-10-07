from flask import jsonify, request
from models import db
from sqlalchemy import text
from ..dao.Album_dao import get_all_albums, get_album_by_id, create_album, update_album, delete_album, insert_album
from flasgger import swag_from

@swag_from({
    'tags': ['Albums'],
    'description': 'Get list of all albums',
    'responses': {
        200: {
            'description': 'List of albums',
            'examples': {
                'application/json': [
                    {"id": 1, "name": "Album1", "length": "45:00", "year": "2020", "artist_id": 1}
                ]
            }
        }
    }
})

def get_albums():
    albums = get_all_albums()
    albums_data = [
        {
            'id': album.id,
            'name': album.name,
            'length': str(album.length),
            'year': str(album.year),
            'artist_id': album.artist_id
        } for album in albums
    ]
    return jsonify(albums_data)

@swag_from({
    'tags': ['Albums'],
    'description': 'Get album by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Album found'},
        404: {'description': 'Album not found'}
    }
})

def get_album(id):
    album = get_album_by_id(id)
    if album:
        album_data = {
            'id': album.id,
            'name': album.name,
            'length': str(album.length),
            'year': str(album.year),
            'artist_id': album.artist_id
        }
        return jsonify(album_data)
    return jsonify({'error': 'Album not found'}), 404

@swag_from({
    'tags': ['Albums'],
    'description': 'Create a new album',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'length': {'type': 'string'},
                    'year': {'type': 'string'},
                    'artist_id': {'type': 'integer'}
                },
                'required': ['name', 'length', 'year', 'artist_id']
            }
        }
    ],
    'responses': {
        201: {'description': 'Album created successfully'}
    }
})

def create_album_route():
    data = request.get_json()
    new_album = create_album(data)
    return jsonify({'message': 'Album created successfully', 'album_id': new_album.id}), 201

@swag_from({
    'tags': ['Albums'],
    'description': 'Update an album by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'length': {'type': 'string'},
                    'year': {'type': 'string'},
                    'artist_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Album updated successfully'},
        404: {'description': 'Album not found'}
    }
})

def update_album_route(id):
    data = request.get_json()
    album = update_album(id, data)
    if album:
        return jsonify({'message': 'Album updated successfully'})
    return jsonify({'error': 'Album not found'}), 404

@swag_from({
    'tags': ['Albums'],
    'description': 'Delete an album by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Album deleted successfully'},
        404: {'description': 'Album not found'},
        500: {'description': 'Failed to delete album'}
    }
})

def delete_album_route(id):
    album = get_album_by_id(id)
    if not album:
        return jsonify({'error': 'Album not found'}), 404

    try:
        db.session.delete(album)
        db.session.commit()
        return jsonify({'message': 'Album deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete album', 'details': str(e)}), 500

def insert_album_route():
    data = request.get_json()

    if not all(key in data for key in ("name", "length", "year", "artist_id")):
        return jsonify({"error": "Missing parameters"}), 400

    name = data['name']
    length = data['length']
    year = data['year']
    artist_id = data['artist_id']

    sql = text("""
            CALL InsertIntoAlbum(:name, :length, :year, :artist_id)
        """)

    try:
        db.session.execute(sql, {'name': name, 'length': length, 'year': year, 'artist_id': artist_id})
        db.session.commit()
        return jsonify({"message": "Album inserted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
