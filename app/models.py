from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Song(db.Model):
    __tablename__ = 'Song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    length = db.Column(db.Time, nullable=False)
    in_playlist = db.Column(db.Boolean, nullable=False)
    lyric = db.Column(db.Text, nullable=False)
    year = db.Column(db.Date, nullable=False)
    genre = db.Column(db.String(45), nullable=False)

    currently_playing = db.relationship('CurrentlyPlaying', backref='song', cascade="all, delete", lazy=True)
    playlists = db.relationship('UserPlaylist', secondary='Song_has_User_playlist', back_populates='songs', cascade="all, delete")
    lyrics = db.relationship('Lyrics', backref='song', cascade="all, delete", lazy=True)
    history = db.relationship('HistoryOfPlayed', secondary='History_of_played_has_Song', back_populates='songs', cascade="all, delete")
    albums = db.relationship('Album', secondary='Album_has_Song', back_populates='songs', cascade="all, delete")
    liked = db.relationship('Liked', secondary='Liked_has_Song', back_populates='songs', cascade="all, delete")
    artists = db.relationship('Artist', secondary='Artist_has_Song', back_populates='songs', cascade="all, delete")
    reviews = db.relationship('Review', backref='song', cascade="all, delete", lazy=True)

class Label(db.Model):
    __tablename__ = 'Label'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(45), nullable=False)

    artists = db.relationship('Artist', backref='label', cascade="all, delete", lazy=True)


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    in_playlist = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(45), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('Label.id'), nullable=False)

    albums = db.relationship('Album', backref='artist', cascade="all, delete", lazy=True)
    songs = db.relationship('Song', secondary='Artist_has_Song', back_populates='artists', cascade="all, delete")


class CurrentlyPlaying(db.Model):
    __tablename__ = 'Currently_playing'
    id = db.Column(db.Integer, primary_key=True)
    is_played_now = db.Column(db.String(45), nullable=False, default='true')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    device = db.Column(db.String(45), nullable=False, unique=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id'), nullable=False)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    genre = db.Column(db.String(45), nullable=False)
    currently_playing_id = db.Column(db.Integer, db.ForeignKey('Currently_playing.id'), nullable=False)

    playlists = db.relationship('UserPlaylist', backref='user', cascade="all, delete", lazy=True)
    history = db.relationship('HistoryOfPlayed', backref='user', cascade="all, delete", lazy=True)
    liked = db.relationship('Liked', backref='user', cascade="all, delete", lazy=True)


class Album(db.Model):
    __tablename__ = 'Album'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    length = db.Column(db.Time, nullable=False)
    year = db.Column(db.Date, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

    songs = db.relationship('Song', secondary='Album_has_Song', back_populates='albums', cascade="all, delete")


class Liked(db.Model):
    __tablename__ = 'Liked'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(45), nullable=False)
    album = db.Column(db.String(45), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    songs = db.relationship('Song', secondary='Liked_has_Song', back_populates='liked', cascade="all, delete")


class UserPlaylist(db.Model):
    __tablename__ = 'User_playlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    name = db.Column(db.String(45), nullable=False)

    songs = db.relationship('Song', secondary='Song_has_User_playlist', back_populates='playlists', cascade="all, delete")


class HistoryOfPlayed(db.Model):
    __tablename__ = 'History_of_played'
    id = db.Column(db.Integer, primary_key=True)
    date_of_playing = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    songs = db.relationship('Song', secondary='History_of_played_has_Song', back_populates='history', cascade="all, delete")

    def __repr__(self):
        return f'<HistoryOfPlayed id={self.id}, date_of_playing={self.date_of_playing}, duration={self.duration}>'

class Lyrics(db.Model):
    __tablename__ = 'Lyrics'
    id = db.Column(db.Integer, primary_key=True)
    lyric = db.Column(db.Text, nullable=False)
    songwriter = db.Column(db.String(45), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id'), nullable=False)

class ArtistHasSong(db.Model):
    __tablename__ = 'Artist_has_Song'
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'), primary_key=True)


class SongHasUserPlaylist(db.Model):
    __tablename__ = 'Song_has_User_playlist'
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'), primary_key=True)
    user_playlist_id = db.Column(db.Integer, db.ForeignKey('User_playlist.id', ondelete='CASCADE'), primary_key=True)


class HistoryOfPlayedHasSong(db.Model):
    __tablename__ = 'History_of_played_has_Song'
    history_of_played_id = db.Column(db.Integer, db.ForeignKey('History_of_played.id', ondelete='CASCADE'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'), primary_key=True)


class AlbumHasSong(db.Model):
    __tablename__ = 'Album_has_Song'
    album_id = db.Column(db.Integer, db.ForeignKey('Album.id', ondelete='CASCADE'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'), primary_key=True)


class LikedHasSong(db.Model):
    __tablename__ = 'Liked_has_Song'
    liked_id = db.Column(db.Integer, db.ForeignKey('Liked.id', ondelete='CASCADE'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.id', ondelete='CASCADE'), primary_key=True)

class Review(db.Model):
    __tablename__ = 'Review'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    Song_id = db.Column(db.Integer, nullable=False)
    User_id = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='reviews', lazy=True)

    def validate_rating(self):
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")

    def __repr__(self):
        return f'<Review {self.id}, Rating: {self.rating}, Song ID: {self.Song_id}, User ID: {self.User_id}>'

class HistoryOfPlayedLog(db.Model):
    __tablename__ = 'HistoryOfPlayedLog'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    history_id = db.Column(db.Integer, db.ForeignKey('History_of_played.id'), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, history_id, deleted_at=None):
        self.history_id = history_id
        if deleted_at is None:
            self.deleted_at = datetime.utcnow()

    def __repr__(self):
        return f'<HistoryOfPlayedLog log_id={self.log_id}, history_id={self.history_id}, deleted_at={self.deleted_at}>'
