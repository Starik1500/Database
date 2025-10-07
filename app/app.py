from flask import Flask, render_template, request, redirect, url_for, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import Config
from models import db
from dotenv import load_dotenv
import os

from my_project.auth.route.Album_route import album_add_routes
from my_project.auth.route.Song_route import song_add_routes
from my_project.auth.route.Artist_route import artist_add_routes
from my_project.auth.route.Album_has_Song_route import album_has_song_add_routes
from my_project.auth.route.Artist_has_Song_route import artist_has_song_add_routes
from my_project.auth.route.Currently_playing_route import currently_playing_add_routes
from my_project.auth.route.History_of_played_route import history_of_played_add_routes
from my_project.auth.route.History_of_played_has_Song_route import history_of_played_has_song_add_routes
from my_project.auth.route.Label_route import label_add_routes
from my_project.auth.route.Liked_route import liked_add_routes
from my_project.auth.route.Liked_has_Song_route import liked_has_song_add_routes
from my_project.auth.route.Lyrics_route import lyrics_add_routes
from my_project.auth.route.Song_has_User_playlist_route import song_has_user_playlist_add_routes
from my_project.auth.route.User_route import user_add_routes
from my_project.auth.route.User_playlist_route import user_playlist_add_routes
from my_project.auth.route.Review_route import review_add_routes
from my_project.auth.route.for_all_route import for_all_add_routes
from my_project.auth.route.History_of_played_log_route import history_of_played_log_routes

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "My API",
        "description": "API з JWT",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [{"Bearer": []}],
}
db.init_app(app)
jwt = JWTManager(app)
swagger = Swagger(app, template=swagger_template)

song_add_routes(app)
album_add_routes(app)
artist_add_routes(app)
album_has_song_add_routes(app)
artist_has_song_add_routes(app)
currently_playing_add_routes(app)
history_of_played_add_routes(app)
history_of_played_has_song_add_routes(app)
label_add_routes(app)
liked_add_routes(app)
liked_has_song_add_routes(app)
lyrics_add_routes(app)
song_has_user_playlist_add_routes(app)
user_add_routes(app)
user_playlist_add_routes(app)
review_add_routes(app)
for_all_add_routes(app)
history_of_played_log_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
