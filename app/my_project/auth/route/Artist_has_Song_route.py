from my_project.auth.controller.Artist_has_Song_controller import (
    get_artist_songs,
    get_song_artists,
    add_artist_has_song,
    delete_artist_has_song,
    get_artist_song_associations_controller,
    insert_into_artist_has_song
)

def artist_has_song_add_routes(app):
    app.add_url_rule('/api/artist_has_song','get_artist_song_associations_controller',get_artist_song_associations_controller,methods=['GET'])
    app.add_url_rule('/api/insert_artist_has_song','insert_into_artist_has_song',insert_into_artist_has_song,methods=['POST'])
