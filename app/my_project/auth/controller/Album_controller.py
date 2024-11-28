from flask import jsonify, request
from models import db
from sqlalchemy import text
from ..dao.Album_dao import get_all_albums, get_album_by_id, create_album, update_album, delete_album, insert_album

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

def create_album_route():
    data = request.get_json()
    new_album = create_album(data)
    return jsonify({'message': 'Album created successfully', 'album_id': new_album.id}), 201

def update_album_route(id):
    data = request.get_json()
    album = update_album(id, data)
    if album:
        return jsonify({'message': 'Album updated successfully'})
    return jsonify({'error': 'Album not found'}), 404

def delete_album_route(id):
    album = get_album_by_id(id)
    if not album:
        return jsonify({'error': 'Album not found'}), 404

    try:
        Song.query.filter_by(album_id=id).delete()
        db.session.commit()

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