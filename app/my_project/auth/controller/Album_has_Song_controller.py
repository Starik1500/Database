from flask import jsonify, request
from ..dao.Album_has_Song_dao import (
    add_album_song,
    get_songs_by_album,
    get_albums_by_song,
    delete_album_song,
    get_album_song_associations
)

def get_album_songs():
    """Retrieve all songs for a specific album."""
    album_id = request.args.get('album_id')
    if album_id:
        songs = get_songs_by_album(album_id)
        songs_data = [{'id': song.id, 'name': song.name} for song in songs]
        return jsonify(songs_data)
    return jsonify({'error': 'album_id parameter is required'}), 400

def get_song_albums():
    """Retrieve all albums containing a specific song."""
    song_id = request.args.get('song_id')
    if song_id:
        albums = get_albums_by_song(song_id)
        albums_data = [{'id': album.id, 'name': album.name} for album in albums]
        return jsonify(albums_data)
    return jsonify({'error': 'song_id parameter is required'}), 400

def add_album_has_song():
    """Add a new album-song association."""
    data = request.get_json()
    album_id = data.get('album_id')
    song_id = data.get('song_id')

    if not album_id or not song_id:
        return jsonify({'error': 'album_id and song_id are required'}), 400

    album_song = add_album_song(album_id, song_id)
    return jsonify({
        'message': 'Album-Song association created successfully',
        'album_id': album_song.album_id,
        'song_id': album_song.song_id
    }), 201

def delete_album_has_song():
    """Delete an album-song association."""
    data = request.get_json()
    album_id = data.get('album_id')
    song_id = data.get('song_id')

    if not album_id or not song_id:
        return jsonify({'error': 'album_id and song_id are required'}), 400

    success = delete_album_song(album_id, song_id)
    if success:
        return jsonify({'message': 'Album-Song association deleted successfully'})
    return jsonify({'error': 'Album-Song association not found'}), 404

def get_album_song_associations_controller():
    """Retrieve album-song associations based on provided filters for album or song."""
    album_id = request.args.get('album_id', type=int)
    song_id = request.args.get('song_id', type=int)

    associations = get_album_song_associations(album_id=album_id, song_id=song_id)

    if album_id and not song_id:
        # Відображаємо лише альбоми з їхніми піснями
        album_data = [
            {
                'id': album.id,
                'name': album.name,
                'length': str(album.length) if album.length else None,
                'year': album.year,
                'artist_id': album.artist_id,
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
            for _, album, _ in associations if album
        ]
        return jsonify(album_data)

    elif song_id and not album_id:
        # Відображаємо лише пісні з їхніми альбомами
        song_data = [
            {
                'id': song.id,
                'name': song.name,
                'length': str(song.length) if song.length else None,
                'lyric': song.lyric,
                'year': song.year,
                'genre': song.genre,
                'albums': [
                    {
                        'id': album.id,
                        'name': album.name,
                        'length': str(album.length) if album.length else None,
                        'year': album.year,
                        'artist_id': album.artist_id
                    }
                    for _, album, _ in associations if album
                ]
            }
            for _, _, song in associations if song
        ]
        return jsonify(song_data)

    else:
        # Якщо немає параметрів або вказані обидва параметри, повертаємо всі зв'язки
        associations_data = [
            {
                'album': {
                    'id': album.id,
                    'name': album.name,
                    'length': str(album.length) if album.length else None,
                    'year': album.year,
                    'artist_id': album.artist_id
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
            for _, album, song in associations
        ]
        return jsonify(associations_data)