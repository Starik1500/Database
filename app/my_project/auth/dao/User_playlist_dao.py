from models import db, UserPlaylist

def create_playlist(name, user_id):
    """Creates a new user playlist."""
    playlist = UserPlaylist(name=name, user_id=user_id)
    db.session.add(playlist)
    db.session.commit()
    return playlist

def get_playlist_by_id(playlist_id):
    """Retrieves a playlist by its ID."""
    return UserPlaylist.query.get(playlist_id)

def get_all_playlists():
    """Returns all user playlists."""
    return UserPlaylist.query.all()

def update_playlist(playlist_id, name, user_id):
    """Updates an existing playlist by its ID."""
    playlist = UserPlaylist.query.get(playlist_id)
    if playlist:
        playlist.name = name
        playlist.user_id = user_id
        db.session.commit()
        return playlist
    return None

def delete_playlist(playlist_id):
    """Deletes a playlist by its ID."""
    playlist = UserPlaylist.query.get(playlist_id)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        return True
    return False

def get_songs_in_playlist(playlist_id):
    playlist = UserPlaylist.query.get(playlist_id)

    # Якщо плейлист не знайдено, повертаємо None
    if playlist is None:
        print(f"Playlist with id {playlist_id} does not exist.")
        return None

    # Повертаємо список пісень у плейлисті
    print(f"Found playlist: {playlist.name} with {len(playlist.songs)} songs.")
    return playlist.songs

