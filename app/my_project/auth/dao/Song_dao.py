from models import db, Song, CurrentlyPlaying, User


def get_all_songs():
    return Song.query.all()


def get_song_by_id(song_id):
    return Song.query.get(song_id)


def create_song(data):
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