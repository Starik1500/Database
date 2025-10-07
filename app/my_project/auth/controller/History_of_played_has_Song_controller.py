from flask import jsonify, request
from ..dao.History_of_played_has_Song_dao import (
    add_history_song,
    get_songs_by_history,
    get_histories_by_song,
    delete_history_song,
    get_history_song_associations
)

def get_songs_by_history_controller():
    """Retrieve all songs associated with a specific history of played entry."""
    history_of_played_id = request.args.get('history_of_played_id')
    if history_of_played_id:
        songs = get_songs_by_history(history_of_played_id)
        songs_data = [{'id': song.id, 'name': song.name} for song in songs]
        return jsonify(songs_data)
    return jsonify({'error': 'history_of_played_id parameter is required'}), 400

def get_histories_by_song_controller():
    """Retrieve all history of played entries associated with a specific song."""
    song_id = request.args.get('song_id')
    if song_id:
        histories = get_histories_by_song(song_id)
        histories_data = [
            {'id': history.id, 'date_of_playing': history.date_of_playing.isoformat() if history.date_of_playing else None, 'duration': str(history.duration) if history.duration else None}
            for history in histories
        ]
        return jsonify(histories_data)
    return jsonify({'error': 'song_id parameter is required'}), 400

def add_history_of_played_has_song():
    """Add a new history of played and song association."""
    data = request.get_json()
    history_of_played_id = data.get('history_of_played_id')
    song_id = data.get('song_id')

    if not history_of_played_id or not song_id:
        return jsonify({'error': 'history_of_played_id and song_id are required'}), 400

    history_song = add_history_song(history_of_played_id, song_id)
    return jsonify({
        'message': 'History-Song association created successfully',
        'history_of_played_id': history_song.history_of_played_id,
        'song_id': history_song.song_id
    }), 201

def delete_history_of_played_has_song():
    """Delete an association between a history of played entry and a song."""
    data = request.get_json()
    history_of_played_id = data.get('history_of_played_id')
    song_id = data.get('song_id')

    if not history_of_played_id or not song_id:
        return jsonify({'error': 'history_of_played_id and song_id are required'}), 400

    success = delete_history_song(history_of_played_id, song_id)
    if success:
        return jsonify({'message': 'History-Song association deleted successfully'})
    return jsonify({'error': 'History-Song association not found'}), 404

def get_history_song_associations_controller():
    """Retrieve history-song associations based on provided filters."""
    history_of_played_id = request.args.get('history_of_played_id', type=int)
    song_id = request.args.get('song_id', type=int)

    associations = get_history_song_associations(history_of_played_id=history_of_played_id, song_id=song_id)

    associations_data = [
        {
            'history': {
                'id': history.id,
                'date_of_playing': history.date_of_playing.isoformat() if history.date_of_playing else None,
                'duration': str(history.duration) if history.duration else None
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
        for _, history, song in associations
    ]
    return jsonify(associations_data)
