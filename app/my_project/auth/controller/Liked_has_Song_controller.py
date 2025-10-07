from flask import jsonify, request
from ..dao.Liked_has_Song_dao import (
    add_liked_song,
    get_songs_by_liked,
    get_liked_by_song,
    delete_liked_song,
    get_liked_song_associations
)

def get_songs_by_liked_controller():
    """Retrieve all songs associated with a specific liked entry."""
    liked_id = request.args.get('liked_id')
    if liked_id:
        songs = get_songs_by_liked(liked_id)
        songs_data = [{'id': song.id, 'name': song.name} for song in songs]
        return jsonify(songs_data)
    return jsonify({'error': 'liked_id parameter is required'}), 400

def get_liked_by_song_controller():
    """Retrieve all liked entries associated with a specific song."""
    song_id = request.args.get('song_id')
    if song_id:
        liked_entries = get_liked_by_song(song_id)
        liked_data = [
            {'id': liked.id, 'artist': liked.artist, 'album': liked.album, 'user_id': liked.user_id}
            for liked in liked_entries
        ]
        return jsonify(liked_data)
    return jsonify({'error': 'song_id parameter is required'}), 400

def add_liked_has_song():
    """Add a new liked-song association."""
    data = request.get_json()
    liked_id = data.get('liked_id')
    song_id = data.get('song_id')

    if not liked_id or not song_id:
        return jsonify({'error': 'liked_id and song_id are required'}), 400

    liked_song = add_liked_song(liked_id, song_id)
    return jsonify({
        'message': 'Liked-Song association created successfully',
        'liked_id': liked_song.liked_id,
        'song_id': liked_song.song_id
    }), 201

def delete_liked_has_song():
    """Delete an association between a liked entry and a song."""
    data = request.get_json()
    liked_id = data.get('liked_id')
    song_id = data.get('song_id')

    if not liked_id or not song_id:
        return jsonify({'error': 'liked_id and song_id are required'}), 400

    success = delete_liked_song(liked_id, song_id)
    if success:
        return jsonify({'message': 'Liked-Song association deleted successfully'})
    return jsonify({'error': 'Liked-Song association not found'}), 404

def get_liked_song_associations_controller():
    """Retrieve liked-song associations based on provided filters."""
    liked_id = request.args.get('liked_id', type=int)
    song_id = request.args.get('song_id', type=int)

    associations = get_liked_song_associations(liked_id=liked_id, song_id=song_id)

    associations_data = [
        {
            'liked': {
                'id': liked.id,
                'artist': liked.artist,
                'album': liked.album,
                'user_id': liked.user_id
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
        for _, liked, song in associations
    ]
    return jsonify(associations_data)
