from models import db, AlbumHasSong, Album, Song
from sqlalchemy.exc import SQLAlchemyError

def add_album_song(album_name, song_name):
    album = Album.query.filter_by(name=album_name).first()
    if not album:
        raise SQLAlchemyError(f"Album '{album_name}' does not exist.")

    song = Song.query.filter_by(name=song_name).first()
    if not song:
        raise SQLAlchemyError(f"Song '{song_name}' does not exist.")

    existing_association = AlbumHasSong.query.filter_by(album_id=album.id, song_id=song.id).first()
    if existing_association:
        raise SQLAlchemyError(f"The album '{album_name}' and song '{song_name}' are already linked.")

    album_song = AlbumHasSong(album_id=album.id, song_id=song.id)
    db.session.add(album_song)
    db.session.commit()
    return album_song

def get_songs_by_album(album_id):
    """Returns all songs belonging to a specified album."""
    return (
        db.session.query(Song)
        .join(AlbumHasSong, AlbumHasSong.song_id == Song.id)
        .filter(AlbumHasSong.album_id == album_id)
        .all()
    )

def get_albums_by_song(song_id):
    """Returns all albums containing a specified song."""
    return (
        db.session.query(Album)
        .join(AlbumHasSong, AlbumHasSong.album_id == Album.id)
        .filter(AlbumHasSong.song_id == song_id)
        .all()
    )

def delete_album_song(album_id, song_id):
    """Deletes the relationship between an album and a song if it exists."""
    album_song = AlbumHasSong.query.filter_by(album_id=album_id, song_id=song_id).first()
    if album_song:
        db.session.delete(album_song)
        db.session.commit()
        return True
    return False

def get_album_song_associations(album_id=None, song_id=None):
    query = db.session.query(AlbumHasSong, Album, Song).join(Album, AlbumHasSong.album_id == Album.id).join(Song, AlbumHasSong.song_id == Song.id)

    if album_id:
        query = query.filter(AlbumHasSong.album_id == album_id)
    if song_id:
        query = query.filter(AlbumHasSong.song_id == song_id)

    return query.all()

