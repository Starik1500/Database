from my_project.auth.controller.Artist_controller import (
    get_artists,
    get_artist,
    create_artist_route,
    update_artist_route,
    delete_artist_route,
    insert_noname_into_artist_route,
    insert_artist_route
)

def artist_add_routes(app):
    app.add_url_rule('/api/artists', 'get_artists', get_artists, methods=['GET'])
    app.add_url_rule('/api/artists/<int:artist_id>', 'get_artist', get_artist, methods=['GET'])
    app.add_url_rule('/api/artists', 'create_artist_route', create_artist_route, methods=['POST'])
    app.add_url_rule('/api/artists_noname', 'insert_noname_into_artist_route', insert_noname_into_artist_route, methods=['POST'])
    app.add_url_rule('/api/artists/<int:artist_id>', 'update_artist_route', update_artist_route, methods=['PUT'])
    app.add_url_rule('/api/artists/<int:artist_id>', 'delete_artist_route', delete_artist_route, methods=['DELETE'])
    app.add_url_rule('/api/insert_artists', 'insert_artist_route', insert_artist_route, methods=['POST'])
