from my_project.auth.controller.History_of_played_has_Song_controller import (
    get_songs_by_history_controller,
    get_histories_by_song_controller,
    add_history_of_played_has_song,
    delete_history_of_played_has_song,
    get_history_song_associations_controller
)

def history_of_played_has_song_add_routes(app):
    app.add_url_rule(
        '/api/history_of_played_has_song',
        'get_history_song_associations_controller',
        get_history_song_associations_controller,
        methods=['GET']
    )