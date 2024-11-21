from flask import jsonify, request
from ..dao.Song_has_User_playlist_dao import (
    add_song_to_playlist,
    get_songs_by_playlist,
    get_playlists_by_song,
    delete_song_from_playlist,
    get_song_playlist_associations
)

def get_songs_by_playlist_controller():
    """Retrieve all songs associated with a specific user playlist."""
    user_playlist_id = request.args.get('user_playlist_id')
    if user_playlist_id:
        songs = get_songs_by_playlist(user_playlist_id)
        songs_data = [{'id': song.id, 'name': song.name} for song in songs]
        return jsonify(songs_data)
    return jsonify({'error': 'user_playlist_id parameter is required'}), 400

def get_playlists_by_song_controller():
    """Retrieve all playlists associated with a specific song."""
    song_id = request.args.get('song_id')
    if song_id:
        playlists = get_playlists_by_song(song_id)
        playlists_data = [{'id': playlist.id, 'name': playlist.name, 'user_id': playlist.user_id} for playlist in playlists]
        return jsonify(playlists_data)
    return jsonify({'error': 'song_id parameter is required'}), 400

def add_song_to_playlist_controller():
    """Add a new song-playlist association."""
    data = request.get_json()
    song_id = data.get('song_id')
    user_playlist_id = data.get('user_playlist_id')

    if not song_id or not user_playlist_id:
        return jsonify({'error': 'song_id and user_playlist_id are required'}), 400

    song_playlist = add_song_to_playlist(song_id, user_playlist_id)
    return jsonify({
        'message': 'Song-Playlist association created successfully',
        'song_id': song_playlist.song_id,
        'user_playlist_id': song_playlist.user_playlist_id
    }), 201

def delete_song_from_playlist_controller():
    """Delete an association between a song and a playlist."""
    data = request.get_json()
    song_id = data.get('song_id')
    user_playlist_id = data.get('user_playlist_id')

    if not song_id or not user_playlist_id:
        return jsonify({'error': 'song_id and user_playlist_id are required'}), 400

    success = delete_song_from_playlist(song_id, user_playlist_id)
    if success:
        return jsonify({'message': 'Song-Playlist association deleted successfully'})
    return jsonify({'error': 'Song-Playlist association not found'}), 404

def get_song_playlist_associations_controller():
    """Retrieve song-playlist associations with optional filtering."""
    song_id = request.args.get('song_id', type=int)
    user_playlist_id = request.args.get('user_playlist_id', type=int)

    associations = get_song_playlist_associations(song_id=song_id, user_playlist_id=user_playlist_id)

    associations_data = [
        {
            'song': {
                'id': song.id,
                'name': song.name,
                'length': str(song.length) if song.length else None,
                'lyric': song.lyric,
                'year': song.year,
                'genre': song.genre
            },
            'playlist': {
                'id': playlist.id,
                'name': playlist.name,
                'user_id': playlist.user_id
            }
        }
        for _, song, playlist in associations
    ]
    return jsonify(associations_data)
