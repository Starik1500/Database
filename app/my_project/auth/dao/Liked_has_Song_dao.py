from models import db, LikedHasSong, Song, Liked

def add_liked_song(liked_id, song_id):
    """Adds a relationship between a liked entry and a song."""
    liked_song = LikedHasSong(liked_id=liked_id, song_id=song_id)
    db.session.add(liked_song)
    db.session.commit()
    return liked_song

def get_songs_by_liked(liked_id):
    """Returns all songs associated with a specific liked entry."""
    return (
        db.session.query(Song)
        .join(LikedHasSong, LikedHasSong.song_id == Song.id)
        .filter(LikedHasSong.liked_id == liked_id)
        .all()
    )

def get_liked_by_song(song_id):
    """Returns all liked entries associated with a specific song."""
    return (
        db.session.query(Liked)
        .join(LikedHasSong, LikedHasSong.liked_id == Liked.id)
        .filter(LikedHasSong.song_id == song_id)
        .all()
    )

def delete_liked_song(liked_id, song_id):
    """Deletes a specific relationship between a liked entry and a song."""
    liked_song = LikedHasSong.query.filter_by(
        liked_id=liked_id,
        song_id=song_id
    ).first()
    if liked_song:
        db.session.delete(liked_song)
        db.session.commit()
        return True
    return False

def get_liked_song_associations(liked_id=None, song_id=None):
    """Returns associations between liked entries and songs with optional filtering."""
    query = (
        db.session.query(LikedHasSong, Liked, Song)
        .join(Liked, LikedHasSong.liked_id == Liked.id)
        .join(Song, LikedHasSong.song_id == Song.id)
    )

    if liked_id:
        query = query.filter(LikedHasSong.liked_id == liked_id)
    if song_id:
        query = query.filter(LikedHasSong.song_id == song_id)

    return query.all()
