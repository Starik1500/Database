from flask import jsonify, request
from ..dao.User_playlist_dao import (
    create_playlist,
    get_playlist_by_id,
    get_all_playlists,
    update_playlist,
    delete_playlist,
    get_songs_in_playlist
)
from ..dao.Song_dao import get_song_by_id
from models import db, SongHasUserPlaylist, Song, UserPlaylist

def get_all_playlists_controller():
    """Retrieve all playlists."""
    playlists = get_all_playlists()
    playlists_data = [
        {'id': playlist.id, 'name': playlist.name, 'user_id': playlist.user_id}
        for playlist in playlists
    ]
    return jsonify(playlists_data)

def get_playlist_controller(playlist_id):
    """Retrieve a playlist by its ID."""
    playlist = get_playlist_by_id(playlist_id)
    if playlist:
        playlist_data = {'id': playlist.id, 'name': playlist.name, 'user_id': playlist.user_id}
        return jsonify(playlist_data)
    return jsonify({'error': 'Playlist not found'}), 404

def add_playlist():
    """Add a new playlist."""
    data = request.get_json()
    name = data.get('name')
    user_id = data.get('user_id')

    if not name or not user_id:
        return jsonify({'error': 'name and user_id are required'}), 400

    playlist = create_playlist(name, user_id)
    return jsonify({
        'message': 'Playlist created successfully',
        'id': playlist.id,
        'name': playlist.name,
        'user_id': playlist.user_id
    }), 201

def update_playlist_controller(playlist_id):
    """Update an existing playlist."""
    data = request.get_json()
    name = data.get('name')
    user_id = data.get('user_id')

    updated_playlist = update_playlist(playlist_id, name, user_id)
    if updated_playlist:
        return jsonify({'message': 'Playlist updated successfully', 'id': updated_playlist.id})
    return jsonify({'error': 'Playlist not found'}), 404

def delete_playlist_controller(playlist_id):
    """Delete a playlist by its ID."""
    success = delete_playlist(playlist_id)
    if success:
        return jsonify({'message': 'Playlist deleted successfully'})
    return jsonify({'error': 'Playlist not found'}), 404

def add_song_to_playlist(playlist_id):
    """Add a song to the specified playlist."""
    data = request.get_json()
    song_id = data.get('song_id')

    if not song_id:
        return jsonify({'error': 'song_id is required'}), 400

    # Перевірка наявності плейлиста
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return jsonify({'error': f'Playlist with id {playlist_id} does not exist'}), 404

    # Перевірка наявності пісні
    song = get_song_by_id(song_id)
    if not song:
        return jsonify({'error': f'Song with id {song_id} does not exist'}), 404

    # Додавання пісні до плейлиста у проміжну таблицю
    try:
        new_entry = SongHasUserPlaylist(user_playlist_id=playlist_id, song_id=song_id)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': f'Song with id {song_id} added to playlist {playlist_id} successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding song to playlist: {e}")
        return jsonify({'error': 'Failed to add song to playlist'}), 500

def get_songs_in_playlist(playlist_id):
    """Retrieve all songs in a specific playlist."""
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return jsonify({'error': f'Playlist with id {playlist_id} does not exist'}), 404

    # Отримання всіх пісень у плейлисті
    songs = SongHasUserPlaylist.query.filter_by(user_playlist_id=playlist_id).all()
    songs_data = [{'song_id': song.song_id} for song in songs]
    return jsonify(songs_data)

def update_song_in_playlist(playlist_id, song_id):
    """Update song in the specified playlist."""
    data = request.get_json()
    new_song_id = data.get('new_song_id')  # Новий song_id, який ми хочемо встановити

    if not new_song_id:
        return jsonify({'error': 'new_song_id is required'}), 400

    # Перевірка наявності плейлиста та пісні
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return jsonify({'error': f'Playlist with id {playlist_id} does not exist'}), 404

    song_association = SongHasUserPlaylist.query.filter_by(user_playlist_id=playlist_id, song_id=song_id).first()
    if not song_association:
        return jsonify({'error': f'Song with id {song_id} is not in playlist {playlist_id}'}), 404

    try:
        # Оновлення song_id на новий
        song_association.song_id = new_song_id
        db.session.commit()
        return jsonify({'message': f'Song in playlist {playlist_id} updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating song in playlist: {e}")
        return jsonify({'error': 'Failed to update song in playlist'}), 500

def delete_song_from_playlist(playlist_id, song_id):
    """Delete a song from the specified playlist."""
    playlist = get_playlist_by_id(playlist_id)
    if not playlist:
        return jsonify({'error': f'Playlist with id {playlist_id} does not exist'}), 404

    song_association = SongHasUserPlaylist.query.filter_by(user_playlist_id=playlist_id, song_id=song_id).first()
    if not song_association:
        return jsonify({'error': f'Song with id {song_id} is not in playlist {playlist_id}'}), 404

    try:
        db.session.delete(song_association)
        db.session.commit()
        return jsonify({'message': f'Song with id {song_id} removed from playlist {playlist_id} successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting song from playlist: {e}")
        return jsonify({'error': 'Failed to delete song from playlist'}), 500

def get_songs_in_playlist_controller(playlist_id):
    """Retrieve all songs in a specific playlist."""
    print(f"Attempting to retrieve songs for playlist_id: {playlist_id}")

    # Отримуємо пісні з DAO
    songs = get_songs_in_playlist(playlist_id)

    # Перевірка на None
    if songs is None:
        print("Playlist not found")
        return jsonify({'message': 'Playlist not found'}), 404

    # Переконайтеся, що songs є списком
    if not isinstance(songs, list):
        print(f"Unexpected data format: {type(songs)}")
        return jsonify({'error': 'Unexpected data format'}), 500

    # Обробка пісень у формат JSON
    songs_data = [
        {
            'id': song.id,
            'name': song.name,
            'length': song.length,
            'lyric': song.lyric,
            'year': song.year,
            'genre': song.genre
        }
        for song in songs
    ]

    if not songs_data:
        print("No songs found in this playlist")
        return jsonify({'message': 'No songs found in this playlist'}), 404

    print("Returning songs data successfully")
    return jsonify(songs_data)