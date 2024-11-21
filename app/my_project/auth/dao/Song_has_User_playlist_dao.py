from models import db, SongHasUserPlaylist, Song, UserPlaylist

def add_song_to_playlist(song_id, user_playlist_id):
    """Adds a relationship between a song and a user playlist."""
    song_playlist = SongHasUserPlaylist(song_id=song_id, user_playlist_id=user_playlist_id)
    db.session.add(song_playlist)
    db.session.commit()
    return song_playlist

def get_songs_by_playlist(user_playlist_id):
    """Returns all songs associated with a specific user playlist."""
    return (
        db.session.query(Song)
        .join(SongHasUserPlaylist, SongHasUserPlaylist.song_id == Song.id)
        .filter(SongHasUserPlaylist.user_playlist_id == user_playlist_id)
        .all()
    )

def get_playlists_by_song(song_id):
    """Returns all playlists associated with a specific song."""
    return (
        db.session.query(UserPlaylist)
        .join(SongHasUserPlaylist, SongHasUserPlaylist.user_playlist_id == UserPlaylist.id)
        .filter(SongHasUserPlaylist.song_id == song_id)
        .all()
    )

def delete_song_from_playlist(song_id, user_playlist_id):
    """Deletes a specific relationship between a song and a user playlist."""
    song_playlist = SongHasUserPlaylist.query.filter_by(song_id=song_id, user_playlist_id=user_playlist_id).first()
    if song_playlist:
        db.session.delete(song_playlist)
        db.session.commit()
        return True
    return False

def get_song_playlist_associations(song_id=None, user_playlist_id=None):
    """Returns associations between songs and playlists with optional filtering."""
    query = (
        db.session.query(SongHasUserPlaylist, Song, UserPlaylist)
        .join(Song, SongHasUserPlaylist.song_id == Song.id)
        .join(UserPlaylist, SongHasUserPlaylist.user_playlist_id == UserPlaylist.id)
    )

    if song_id:
        query = query.filter(SongHasUserPlaylist.song_id == song_id)
    if user_playlist_id:
        query = query.filter(SongHasUserPlaylist.user_playlist_id == user_playlist_id)

    return query.all()
