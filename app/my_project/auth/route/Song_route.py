from my_project.auth.controller.Song_controller import get_songs, get_song, create_song_route, update_song_route, delete_song_route, get_playlists_for_song_controller

def song_add_routes(app):
    app.add_url_rule('/api/songs', 'get_songs', get_songs, methods=['GET'])
    app.add_url_rule('/api/songs/<int:id>', 'get_song', get_song, methods=['GET'])
    app.add_url_rule('/api/songs', 'create_song_route', create_song_route, methods=['POST'])
    app.add_url_rule('/api/songs/<int:id>', 'update_song_route', update_song_route, methods=['PUT'])
    app.add_url_rule('/api/songs/<int:id>', 'delete_song_route', delete_song_route, methods=['DELETE'])
    app.add_url_rule('/api/songs/<int:song_id>/playlists', 'get_playlists_for_song', get_playlists_for_song_controller,
                     methods=['GET'])