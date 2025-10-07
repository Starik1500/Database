from my_project.auth.controller.History_of_played_log_controller import (
    get_logs,
    add_history,
    delete_history
)

def history_of_played_log_routes(app):
    app.add_url_rule('/api/history_of_played_log', 'get_all_history_logs', get_logs, methods=['GET'])
    app.add_url_rule('/api/history_of_played_log', 'add_history', add_history, methods=['POST'])
    app.add_url_rule('/api/history_of_played_log/<int:log_id>', 'delete_history', delete_history, methods=['DELETE'])
