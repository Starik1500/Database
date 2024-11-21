from flask import jsonify, request
from ..dao.Song_dao import get_all_songs, get_song_by_id, create_song, update_song, delete_song, get_playlists_for_song

def get_songs():
    songs = get_all_songs()
    songs_data = [
        {
            'id': song.id,
            'name': song.name,
            'length': str(song.length),
            'in_playlist': song.in_playlist,
            'lyric': song.lyric,
            'year': str(song.year),
            'genre': song.genre
        } for song in songs
    ]
    return jsonify(songs_data)

def get_song(id):
    song = get_song_by_id(id)
    if song:
        song_data = {
            'id': song.id,
            'name': song.name,
            'length': str(song.length),
            'in_playlist': song.in_playlist,
            'lyric': song.lyric,
            'year': str(song.year),
            'genre': song.genre
        }
        return jsonify(song_data)
    return jsonify({'error': 'Song not found'}), 404

def create_song_route():
    data = request.get_json()
    new_song = create_song(data)
    return jsonify({'message': 'Song created successfully', 'song_id': new_song.id}), 201

def update_song_route(id):
    data = request.get_json()
    song = update_song(id, data)
    if song:
        return jsonify({'message': 'Song updated successfully'})
    return jsonify({'error': 'Song not found'}), 404

def delete_song_route(id):
    song = delete_song(id)
    if song:
        return jsonify({'message': 'Song deleted successfully'})
    return jsonify({'error': 'Song not found'}), 404

def get_playlists_for_song_controller(song_id):
    """Retrieve all playlists that contain a specific song."""
    playlists = get_playlists_for_song(song_id)

    playlists_data = [
        {
            'id': playlist.id,
            'name': playlist.name,
            'user_id': playlist.user_id
        }
        for playlist in playlists
    ]

    if not playlists_data:
        return jsonify({'message': 'No playlists found for this song'}), 404

    return jsonify(playlists_data)