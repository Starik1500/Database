from models import db, Song, CurrentlyPlaying, User
from sqlalchemy.exc import SQLAlchemyError

def prevent_song_modifications():
    raise SQLAlchemyError("Modifications to the Song table are not allowed.")

def get_all_songs():
    return Song.query.all()


def get_song_by_id(song_id):
    return Song.query.get(song_id)


def create_song(data):
    prevent_song_modifications()
    new_song = Song(
        name=data['name'],
        length=data['length'],
        in_playlist=data.get('in_playlist', False),
        lyric=data['lyric'],
        year=data['year'],
        genre=data['genre']
    )
    db.session.add(new_song)
    db.session.commit()
    return new_song


def update_song(song_id, data):
    prevent_song_modifications()
    song = Song.query.get(song_id)
    if not song:
        return None

    song.name = data.get('name', song.name)
    song.length = data.get('length', song.length)
    song.in_playlist = data.get('in_playlist', song.in_playlist)
    song.lyric = data.get('lyric', song.lyric)
    song.year = data.get('year', song.year)
    song.genre = data.get('genre', song.genre)

    db.session.commit()
    return song


def delete_song(song_id):
    prevent_song_modifications()
    song = Song.query.get(song_id)
    if song:
        CurrentlyPlaying.query.filter_by(song_id=song_id).delete()
        db.session.delete(song)
        db.session.commit()
    return song

def get_playlists_for_song(song_id):
    """Returns all playlists that contain a specific song."""
    song = Song.query.get(song_id)
    return song.playlists if song else []

def insert_song(name, length, in_playlist, lyric, year, genre):
    prevent_song_modifications()
    try:
        db.session.execute("""
                CALL InsertIntoSong(:name, :length, :in_playlist, :lyric, :year, :genre)
            """, {'name': name, 'length': length, 'in_playlist': in_playlist, 'lyric': lyric, 'year': year,
                  'genre': genre})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e