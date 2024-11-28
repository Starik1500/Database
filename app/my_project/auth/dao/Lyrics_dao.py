from models import db, Lyrics
from sqlalchemy import text

def insert_lyrics_in_dao(lyric, songwriter, song_id):
    try:
        sql = text("""
            INSERT INTO Lyrics (lyric, songwriter, song_id)
            VALUES (:lyric, :songwriter, :song_id)
        """)

        # Виконання параметризованого SQL-запиту
        db.session.execute(sql, {
            'lyric': lyric,
            'songwriter': songwriter,
            'song_id': song_id
        })

        db.session.commit()  # Коміт змін у базі даних
        return {"message": "Lyrics entry created successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to insert record: {str(e)}"}

def create_lyrics(lyric, songwriter, song_id):
    lyrics = Lyrics(lyric=lyric, songwriter=songwriter, song_id=song_id)
    db.session.add(lyrics)
    db.session.commit()
    return lyrics

def get_lyrics_by_id(lyrics_id):
    """Retrieves a lyrics entry by its ID."""
    return Lyrics.query.get(lyrics_id)

def get_all_lyrics():
    """Returns all lyrics entries."""
    return Lyrics.query.all()

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
