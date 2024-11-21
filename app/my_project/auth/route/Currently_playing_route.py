from my_project.auth.controller.Currently_playing_controller import (
    get_all_currently_playing,
    get_currently_playing,
    add_currently_playing,
    update_currently_playing,
    delete_currently_playing
)

def currently_playing_add_routes(app):
    app.add_url_rule('/api/currently_playing', 'get_all_currently_playing', get_all_currently_playing, methods=['GET'])
    app.add_url_rule('/api/currently_playing/<int:currently_playing_id>', 'get_currently_playing', get_currently_playing, methods=['GET'])
    app.add_url_rule('/api/currently_playing', 'add_currently_playing', add_currently_playing, methods=['POST'])
    app.add_url_rule('/api/currently_playing/<int:currently_playing_id>', 'update_currently_playing', update_currently_playing, methods=['PUT'])
    app.add_url_rule('/api/currently_playing/<int:currently_playing_id>', 'delete_currently_playing', delete_currently_playing, methods=['DELETE'])
