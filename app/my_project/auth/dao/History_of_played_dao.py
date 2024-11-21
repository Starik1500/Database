from models import db, HistoryOfPlayed

def create_history_of_played(date_of_playing, duration, user_id):
    """Creates a new history of played entry."""
    history_of_played = HistoryOfPlayed(
        date_of_playing=date_of_playing,
        duration=duration,
        user_id=user_id
    )
    db.session.add(history_of_played)
    db.session.commit()
    return history_of_played.id

def get_history_of_played_by_id(history_id):
    """Retrieves a history of played entry by its ID."""
    return HistoryOfPlayed.query.get(history_id)

def get_all_history_of_played():
    """Returns all history of played entries."""
    return HistoryOfPlayed.query.all()

def update_history_of_played(history_id, date_of_playing, duration, user_id):
    """Updates a history of played entry by its ID."""
    history_of_played = HistoryOfPlayed.query.get(history_id)
    if history_of_played:
        history_of_played.date_of_playing = date_of_playing
        history_of_played.duration = duration
        history_of_played.user_id = user_id
        db.session.commit()
        return True
    return False

def delete_history_of_played(history_id):
    """Deletes a history of played entry by its ID."""
    history_of_played = HistoryOfPlayed.query.get(history_id)
    if history_of_played:
        db.session.delete(history_of_played)
        db.session.commit()
        return True
    return False
