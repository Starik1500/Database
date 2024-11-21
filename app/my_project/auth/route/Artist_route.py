from my_project.auth.controller.Artist_controller import (
    get_artists,
    get_artist,
    create_artist_route,
    update_artist_route,
    delete_artist_route
)

def artist_add_routes(app):
    app.add_url_rule('/api/artists', 'get_artists', get_artists, methods=['GET'])
    app.add_url_rule('/api/artists/<int:artist_id>', 'get_artist', get_artist, methods=['GET'])
    app.add_url_rule('/api/artists', 'create_artist_route', create_artist_route, methods=['POST'])
    app.add_url_rule('/api/artists/<int:artist_id>', 'update_artist_route', update_artist_route, methods=['PUT'])
    app.add_url_rule('/api/artists/<int:artist_id>', 'delete_artist_route', delete_artist_route, methods=['DELETE'])
