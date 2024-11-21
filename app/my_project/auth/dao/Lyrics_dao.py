from models import db, Lyric

def create_lyrics(lyric, songwriter, song_id):
    """Creates a new lyrics entry."""
    lyrics = Lyrics(lyric=lyric, songwriter=songwriter, song_id=song_id)
    db.session.add(lyrics)
    db.session.commit()
    return lyrics

def get_lyrics_by_id(lyrics_id):
    """Retrieves a lyrics entry by its ID."""
    return Lyric.query.get(lyrics_id)

def get_all_lyrics():
    """Returns all lyrics entries."""
    return Lyric.query.all()

def update_lyrics(lyrics_id, lyric, songwriter, song_id):
    """Updates an existing lyrics entry by its ID."""
    lyrics = Lyrics.query.get(lyrics_id)
    if lyrics:
        lyrics.lyric = lyric
        lyrics.songwriter = songwriter
        lyrics.song_id = song_id
        db.session.commit()
        return lyrics
    return None

def delete_lyrics(lyrics_id):
    """Deletes a lyrics entry by its ID."""
    lyrics = Lyrics.query.get(lyrics_id)
    if lyrics:
        db.session.delete(lyrics)
        db.session.commit()
        return True
    return False
