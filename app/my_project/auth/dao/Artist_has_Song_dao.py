from models import db, ArtistHasSong, Artist, Song

def add_artist_song(artist_id, song_id):
    """Adds a relationship between an artist and a song."""
    artist_song = ArtistHasSong(artist_id=artist_id, song_id=song_id)
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
    """Returns artist-song associations with optional filtering by artist_id or song_id."""
    query = (
        db.session.query(ArtistHasSong, Artist, Song)
        .join(Artist, ArtistHasSong.artist_id == Artist.id)
        .join(Song, ArtistHasSong.song_id == Song.id)
    )

    if artist_id:
        query = query.filter(ArtistHasSong.artist_id == artist_id)
    if song_id:
        query = query.filter(ArtistHasSong.song_id == song_id)

    return query.all()
