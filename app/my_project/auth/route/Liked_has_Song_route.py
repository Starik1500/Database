from my_project.auth.controller.Liked_has_Song_controller import (
    get_songs_by_liked_controller,
    get_liked_by_song_controller,
    add_liked_has_song,
    delete_liked_has_song,
    get_liked_song_associations_controller
)

def liked_has_song_add_routes(app):
    """Add routes for Liked-Song associations."""
    app.add_url_rule(
        '/api/liked_has_song',
        'get_liked_song_associations_controller',
        get_liked_song_associations_controller,
        methods=['GET']
    )