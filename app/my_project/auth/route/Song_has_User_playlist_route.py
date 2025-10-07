from my_project.auth.controller.Song_has_User_playlist_controller import (
    get_songs_by_playlist_controller,
    get_playlists_by_song_controller,
    add_song_to_playlist_controller,
    delete_song_from_playlist_controller,
    get_song_playlist_associations_controller
)


def song_has_user_playlist_add_routes(app):
    app.add_url_rule(
        '/api/song_has_playlist',
        'get_song_playlist_associations_controller',
        get_song_playlist_associations_controller,
        methods=['GET']
    )