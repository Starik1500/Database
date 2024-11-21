from my_project.auth.controller.User_playlist_controller import (
    get_all_playlists_controller,
    get_playlist_controller,
    add_playlist,
    update_playlist_controller,
    delete_playlist_controller,
    add_song_to_playlist,
    get_songs_in_playlist,
    update_song_in_playlist,
    delete_song_from_playlist,
    get_songs_in_playlist_controller
)

def user_playlist_add_routes(app):
    app.add_url_rule('/api/playlists', 'get_all_playlists_controller', get_all_playlists_controller, methods=['GET'])
    app.add_url_rule('/api/playlists/<int:playlist_id>', 'get_playlist_controller', get_playlist_controller, methods=['GET'])
    app.add_url_rule('/api/playlists', 'add_playlist', add_playlist, methods=['POST'])
    app.add_url_rule('/api/playlists/<int:playlist_id>', 'update_playlist_controller', update_playlist_controller, methods=['PUT'])
    app.add_url_rule('/api/playlists/<int:playlist_id>', 'delete_playlist_controller', delete_playlist_controller, methods=['DELETE'])
    app.add_url_rule('/api/playlists/<int:playlist_id>/songs', 'get_songs_in_playlist', get_songs_in_playlist_controller, methods=['GET'])
