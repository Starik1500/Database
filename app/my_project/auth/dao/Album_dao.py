from models import db, Album

def get_all_albums():
    return Album.query.all()

def get_album_by_id(album_id):
    return Album.query.get(album_id)

def create_album(data):
    new_album = Album(
        name=data['name'],
        length=data['length'],
        year=data['year'],
        artist_id=data['artist_id']
    )
    db.session.add(new_album)
    db.session.commit()
    return new_album

def update_album(album_id, data):
    album = Album.query.get(album_id)
    if not album:
        return None

    album.name = data.get('name', album.name)
    album.length = data.get('length', album.length)
    album.year = data.get('year', album.year)
    album.artist_id = data.get('artist_id', album.artist_id)

    db.session.commit()
    return album

def delete_album(album_id):
    album = Album.query.get(album_id)
    if album:
        db.session.delete(album)
        db.session.commit()
    return album

def insert_album(name, length, year, artist_id):
    try:
        db.session.execute("""
                CALL InsertIntoAlbum(:name, :length, :year, :artist_id)
            """, {'name': name, 'length': length, 'year': year, 'artist_id': artist_id})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e