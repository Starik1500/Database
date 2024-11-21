from models import db, Artist

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