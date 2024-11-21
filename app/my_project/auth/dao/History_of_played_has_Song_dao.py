from models import db, HistoryOfPlayedHasSong, Song, HistoryOfPlayed

def add_history_song(history_of_played_id, song_id):
    """Adds a relationship between a history of played entry and a song."""
    history_song = HistoryOfPlayedHasSong(
        history_of_played_id=history_of_played_id,
        song_id=song_id
    )
    db.session.add(history_song)
    db.session.commit()
    return history_song

def get_songs_by_history(history_of_played_id):
    """Returns all songs associated with a specific history of played entry."""
    return (
        db.session.query(Song)
        .join(HistoryOfPlayedHasSong, HistoryOfPlayedHasSong.song_id == Song.id)
        .filter(HistoryOfPlayedHasSong.history_of_played_id == history_of_played_id)
        .all()
    )

def get_histories_by_song(song_id):
    """Returns all history of played entries associated with a specific song."""
    return (
        db.session.query(HistoryOfPlayed)
        .join(HistoryOfPlayedHasSong, HistoryOfPlayedHasSong.history_of_played_id == HistoryOfPlayed.id)
        .filter(HistoryOfPlayedHasSong.song_id == song_id)
        .all()
    )

def delete_history_song(history_of_played_id, song_id):
    """Deletes a specific relationship between a history of played entry and a song."""
    history_song = HistoryOfPlayedHasSong.query.filter_by(
        history_of_played_id=history_of_played_id,
        song_id=song_id
    ).first()
    if history_song:
        db.session.delete(history_song)
        db.session.commit()
        return True
    return False

def get_history_song_associations(history_of_played_id=None, song_id=None):
    """Returns associations between history of played entries and songs with optional filtering."""
    query = (
        db.session.query(HistoryOfPlayedHasSong, HistoryOfPlayed, Song)
        .join(HistoryOfPlayed, HistoryOfPlayedHasSong.history_of_played_id == HistoryOfPlayed.id)
        .join(Song, HistoryOfPlayedHasSong.song_id == Song.id)
    )

    if history_of_played_id:
        query = query.filter(HistoryOfPlayedHasSong.history_of_played_id == history_of_played_id)
    if song_id:
        query = query.filter(HistoryOfPlayedHasSong.song_id == song_id)

    return query.all()
