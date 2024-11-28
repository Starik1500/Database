from models import db, Artist
from sqlalchemy import text

def get_all_artists():
    return Artist.query.all()

def get_artist_by_id(artist_id):
    return Artist.query.get(artist_id)

def create_artist(data):
    artist = Artist(
        name=data['name'],
        in_playlist=data.get('in_playlist', False),
        genre=data['genre'],
        label_id=data['label_id']
    )
    db.session.add(artist)
    db.session.commit()
    return artist

def update_artist(artist_id, data):
    artist = Artist.query.get(artist_id)
    if artist:
        artist.name = data.get('name', artist.name)
        artist.in_playlist = data.get('in_playlist', artist.in_playlist)
        artist.genre = data.get('genre', artist.genre)
        artist.label_id = data.get('label_id', artist.label_id)
        db.session.commit()
        return artist
    return None

def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        db.session.delete(artist)
        db.session.commit()
        return artist
    return None

def insert_noname_into_artist():
    try:
        result = db.session.execute(text(f"CALL InsertNonameIntoTable(:table_name)"), {'table_name': 'artist'})
        db.session.commit()

        return {"message": "Procedure executed for table: artist"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

def insert_artist(genre, artist_id, in_playlist, label_id, name):
    try:
        # Параметризований SQL запит для вставки даних
        sql = text("""
                INSERT INTO Artist (genre, id, in_playlist, label_id, name)
                VALUES (:genre, :id, :in_playlist, :label_id, :name)
            """)

        # Виконання запиту з передачею параметрів
        db.session.execute(sql, {
            'genre': genre,
            'id': artist_id,
            'in_playlist': in_playlist,
            'label_id': label_id,
            'name': name
        })
        db.session.commit()  # Підтверджуємо зміни в базі даних
        return {"message": "Artist inserted successfully"}

    except Exception as e:
        db.session.rollback()  # Якщо сталася помилка, скасовуємо зміни
        return {"error": str(e)}