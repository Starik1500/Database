from models import db, CurrentlyPlaying
from sqlalchemy import text
from datetime import datetime

def create_currently_playing(is_played_now, timestamp, device, song_id):
    """Creates a new currently playing entry."""
    currently_playing = CurrentlyPlaying(
        is_played_now=is_played_now,
        timestamp=timestamp,
        device=device,
        song_id=song_id
    )
    db.session.add(currently_playing)
    db.session.commit()
    return currently_playing

def get_currently_playing_by_id(currently_playing_id):
    """Retrieves a currently playing entry by its ID."""
    return CurrentlyPlaying.query.get(currently_playing_id)

def get_all_currently_playing():
    """Returns all currently playing entries."""
    return CurrentlyPlaying.query.all()

def delete_currently_playing(currently_playing_id):
    """Deletes a currently playing entry by its ID."""
    currently_playing = CurrentlyPlaying.query.get(currently_playing_id)
    if currently_playing:
        db.session.delete(currently_playing)
        db.session.commit()
        return True
    return False


def insert_currently_playing(is_played_now, timestamp, device, song_id):
    """Inserts a new record into the 'CurrentlyPlaying' table using a parameterized query."""
    try:
        # SQL-запит для вставки нового запису
        sql = text("""
            INSERT INTO Currently_playing (is_played_now, timestamp, device, song_id)
            VALUES (:is_played_now, :timestamp, :device, :song_id)
        """)

        # Виконання запиту з параметрами
        db.session.execute(sql, {
            'is_played_now': is_played_now,
            'timestamp': timestamp,
            'device': device,
            'song_id': song_id
        })

        # Збереження змін у базі даних
        db.session.commit()
        return {"message": "Currently playing entry created successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to insert record: {str(e)}"}