from flask import jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models import db
from ..dao.Artist_has_Song_dao import (
    add_artist_song,
    get_songs_by_artist,
    get_artists_by_song,
    delete_artist_song,
    get_artist_song_associations
)

def insert_into_artist_has_song():
    data = request.get_json()

    if not all(key in data for key in ("artist_name", "song_name")):
        return jsonify({"error": "Missing parameters"}), 400

    artist_name = data['artist_name']
    song_name = data['song_name']

    try:
        artist_song = add_artist_song(artist_name, song_name)
        return jsonify({
            "message": "Song linked to artist successfully",
            "artist_id": artist_song.artist_id,
            "song_id": artist_song.song_id
        }), 201

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An error occurred while processing the request"}), 500

def get_artist_songs():
    """Retrieve all songs for a specific artist."""
    artist_id = request.args.get('artist_id')
    if artist_id:
        songs = get_songs_by_artist(artist_id)
        songs_data = [{'id': song.id, 'name': song.name} for song in songs]
        return jsonify(songs_data)
    return jsonify({'error': 'artist_id parameter is required'}), 400

def get_song_artists():
    """Retrieve all artists associated with a specific song."""
    song_id = request.args.get('song_id')
    if song_id:
        artists = get_artists_by_song(song_id)
        artists_data = [{'id': artist.id, 'name': artist.name} for artist in artists]
        return jsonify(artists_data)
    return jsonify({'error': 'song_id parameter is required'}), 400

def add_artist_has_song():
    """Add a new artist-song association."""
    data = request.get_json()
    artist_id = data.get('artist_id')
    song_id = data.get('song_id')

    if not artist_id or not song_id:
        return jsonify({'error': 'artist_id and song_id are required'}), 400

    artist_song = add_artist_song(artist_id, song_id)
    return jsonify({
        'message': 'Artist-Song association created successfully',
        'artist_id': artist_song.artist_id,
        'song_id': artist_song.song_id
    }), 201

def delete_artist_has_song():
    """Delete an artist-song association."""
    data = request.get_json()
    artist_id = data.get('artist_id')
    song_id = data.get('song_id')

    if not artist_id or not song_id:
        return jsonify({'error': 'artist_id and song_id are required'}), 400

    success = delete_artist_song(artist_id, song_id)
    if success:
        return jsonify({'message': 'Artist-Song association deleted successfully'})
    return jsonify({'error': 'Artist-Song association not found'}), 404

def get_artist_song_associations_controller():
    """Retrieve artist-song associations based on provided filters for artist or song."""
    artist_id = request.args.get('artist_id', type=int)
    song_id = request.args.get('song_id', type=int)

    associations = get_artist_song_associations(artist_id=artist_id, song_id=song_id)

    if artist_id and not song_id:
        # Display only artists with their songs
        artist_data = [
            {
                'id': artist.id,
                'name': artist.name,
                'genre': artist.genre,
                'songs': [
                    {
                        'id': song.id,
                        'name': song.name,
                        'length': str(song.length) if song.length else None,
                        'lyric': song.lyric,
                        'year': song.year,
                        'genre': song.genre
                    }
                    for _, _, song in associations if song
                ]
            }
            for _, artist, _ in associations if artist
        ]
        return jsonify(artist_data)

    elif song_id and not artist_id:
        # Display only songs with their artists
        song_data = [
            {
                'id': song.id,
                'name': song.name,
                'length': str(song.length) if song.length else None,
                'lyric': song.lyric,
                'year': song.year,
                'genre': song.genre,
                'artists': [
                    {
                        'id': artist.id,
                        'name': artist.name,
                        'genre': artist.genre
                    }
                    for _, artist, _ in associations if artist
                ]
            }
            for _, _, song in associations if song
        ]
        return jsonify(song_data)

    else:
        # If no parameters or both are specified, return all associations
        associations_data = [
            {
                'artist': {
                    'id': artist.id,
                    'name': artist.name,
                    'genre': artist.genre
                },
                'song': {
                    'id': song.id,
                    'name': song.name,
                    'length': str(song.length) if song.length else None,
                    'lyric': song.lyric,
                    'year': song.year,
                    'genre': song.genre
                }
            }
            for _, artist, song in associations
        ]
        return jsonify(associations_data)


def insert_into_artist_has_song():
    data = request.get_json()

    if not all(key in data for key in ("artist_name", "song_name")):
        return jsonify({"error": "Missing parameters"}), 400

    artist_name = data['artist_name']
    song_name = data['song_name']

    sql = text("""
        CALL InsertIntoArtistHasSong(:artist_name, :song_name)
    """)

    try:
        db.session.execute(sql, {'artist_name': artist_name, 'song_name': song_name})
        db.session.commit()
        return jsonify({"message": "Song linked to artist successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
