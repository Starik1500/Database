from my_project.auth.controller.History_of_played_controller import (
    get_all_history_of_played,
    get_history_of_played,
    add_history_of_played,
    update_history_of_played,
    delete_history_of_played
)

def history_of_played_add_routes(app):
    app.add_url_rule('/api/history_of_played', 'get_all_history_of_played', get_all_history_of_played, methods=['GET'])
    app.add_url_rule('/api/history_of_played/<int:history_id>', 'get_history_of_played', get_history_of_played, methods=['GET'])
    app.add_url_rule('/api/history_of_played', 'add_history_of_played', add_history_of_played, methods=['POST'])
    app.add_url_rule('/api/history_of_played/<int:history_id>', 'update_history_of_played', update_history_of_played, methods=['PUT'])
    app.add_url_rule('/api/history_of_played/<int:history_id>', 'delete_history_of_played', delete_history_of_played, methods=['DELETE'])
