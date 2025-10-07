from models import db, ArtistHasSong, Artist, Song
from sqlalchemy.exc import SQLAlchemyError

def add_artist_song(artist_name, song_name):
    artist = Artist.query.filter_by(name=artist_name).first()
    if not artist:
        raise SQLAlchemyError(f"Artist '{artist_name}' does not exist.")

    song = Song.query.filter_by(name=song_name).first()
    if not song:
        raise SQLAlchemyError(f"Song '{song_name}' does not exist.")

    existing_association = AlbumHasSong.query.filter_by(artist_id=artist.id, song_id=song.id).first()
    if existing_association:
        raise SQLAlchemyError(f"The Artist '{artist_name}' and song '{song_name}' are already linked.")

    artist_song = AlbumHasSong(artist_id=artist.id, song_id=song.id)
    db.session.add(artist_song)
    db.session.commit()
    return artist_song

def get_songs_by_artist(artist_id):
    """Returns all songs associated with a specified artist."""
    return (
        db.session.query(Song)
        .join(ArtistHasSong, ArtistHasSong.song_id == Song.id)
        .filter(ArtistHasSong.artist_id == artist_id)
        .all()
    )

def get_artists_by_song(song_id):
    """Returns all artists associated with a specified song."""
    return (
        db.session.query(Artist)
        .join(ArtistHasSong, ArtistHasSong.artist_id == Artist.id)
        .filter(ArtistHasSong.song_id == song_id)
        .all()
    )

def delete_artist_song(artist_id, song_id):
    """Deletes the relationship between an artist and a song if it exists."""
    artist_song = ArtistHasSong.query.filter_by(artist_id=artist_id, song_id=song_id).first()
    if artist_song:
        db.session.delete(artist_song)
        db.session.commit()
        return True
    return False

def get_artist_song_associations(artist_id=None, song_id=None):
    query = db.session.query(ArtistHasSong, Artist, Song).join(Artist, ArtistHasSong.artist_id == Artist.id).join(Song, ArtistHasSong.song_id == Song.id)

    if artist_id:
        query = query.filter(ArtistHasSong.artist_id == artist_id)
    if song_id:
        query = query.filter(ArtistHasSong.song_id == song_id)

    return query.all()
