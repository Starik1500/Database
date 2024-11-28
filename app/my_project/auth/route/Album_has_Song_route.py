from my_project.auth.controller.Album_has_Song_controller import (
    get_album_songs,
    get_song_albums,
    get_album_song_associations_controller,
    insert_into_album_has_song
)

def album_has_song_add_routes(app):
    app.add_url_rule('/api/album_has_song', 'get_album_song_associations_controller', get_album_song_associations_controller, methods=['GET'])
    app.add_url_rule('/api/insert_album_has_song', 'insert_into_album_has_song', insert_into_album_has_song,
                     methods=['POST'])