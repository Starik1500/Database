from flask_jwt_extended import jwt_required
from my_project.auth.controller.Album_controller import (
    get_albums,
    get_album,
    create_album_route,
    update_album_route,
    delete_album_route,
    insert_album_route
)

def album_add_routes(app):
    app.add_url_rule('/api/albums', 'get_albums', jwt_required()(get_albums), methods=['GET'])
    app.add_url_rule('/api/albums/<int:id>', 'get_album', jwt_required()(get_album), methods=['GET'])
    app.add_url_rule('/api/albums', 'create_album_route', jwt_required()(create_album_route), methods=['POST'])
    app.add_url_rule('/api/albums/<int:id>', 'update_album_route', jwt_required()(update_album_route), methods=['PUT'])
    app.add_url_rule('/api/albums/<int:id>', 'delete_album_route', jwt_required()(delete_album_route), methods=['DELETE'])
    app.add_url_rule('/api/insert_album', 'insert_album_route', jwt_required()(insert_album_route), methods=['POST'])
