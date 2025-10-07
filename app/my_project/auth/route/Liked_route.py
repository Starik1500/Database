from my_project.auth.controller.Liked_controller import (
    get_all_liked,
    get_liked,
    add_liked,
    update_liked,
    delete_liked
)

def liked_add_routes(app):
    app.add_url_rule('/api/liked', 'get_all_liked', get_all_liked, methods=['GET'])
    app.add_url_rule('/api/liked/<int:liked_id>', 'get_liked', get_liked, methods=['GET'])
    app.add_url_rule('/api/liked', 'add_liked', add_liked, methods=['POST'])
    app.add_url_rule('/api/liked/<int:liked_id>', 'update_liked', update_liked, methods=['PUT'])
    app.add_url_rule('/api/liked/<int:liked_id>', 'delete_liked', delete_liked, methods=['DELETE'])
