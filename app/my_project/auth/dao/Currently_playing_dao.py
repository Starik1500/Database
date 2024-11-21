from models import db, CurrentlyPlaying

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
