from models import db, Liked
from sqlalchemy import text

def insert_liked_in_dao(artist, album, user_id):
    """Параметризована вставка для таблиці 'Liked'."""
    try:
        sql = text("""
            INSERT INTO Liked (artist, album, user_id)
            VALUES (:artist, :album, :user_id)
        """)

        # Виконання параметризованого SQL-запиту
        db.session.execute(sql, {
            'artist': artist,
            'album': album,
            'user_id': user_id
        })

        db.session.commit()  # Коміт змін у базі даних
        return {"message": "Liked entry created successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to insert record: {str(e)}"}

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
