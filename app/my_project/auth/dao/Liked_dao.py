from models import db, Liked

def create_liked(artist, album, user_id):
    """Creates a new liked entry."""
    liked = Liked(artist=artist, album=album, user_id=user_id)
    db.session.add(liked)
    db.session.commit()
    return liked

def get_liked_by_id(liked_id):
    """Retrieves a liked entry by its ID."""
    return Liked.query.get(liked_id)

def get_all_liked():
    """Returns all liked entries."""
    return Liked.query.all()

def update_liked(liked_id, artist, album, user_id):
    """Updates an existing liked entry by its ID."""
    liked = Liked.query.get(liked_id)
    if liked:
        liked.artist = artist
        liked.album = album
        liked.user_id = user_id
        db.session.commit()
        return liked
    return None

def delete_liked(liked_id):
    """Deletes a liked entry by its ID."""
    liked = Liked.query.get(liked_id)
    if liked:
        db.session.delete(liked)
        db.session.commit()
        return True
    return False
