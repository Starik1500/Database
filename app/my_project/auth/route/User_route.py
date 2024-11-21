from my_project.auth.controller.User_controller import (
    get_all_users_controller,
    get_user_controller,
    add_user,
    update_user_controller,
    delete_user_controller
)

def user_add_routes(app):
    app.add_url_rule('/api/users', 'get_all_users_controller', get_all_users_controller, methods=['GET'])
    app.add_url_rule('/api/users/<int:user_id>', 'get_user_controller', get_user_controller, methods=['GET'])
    app.add_url_rule('/api/users', 'add_user', add_user, methods=['POST'])
    app.add_url_rule('/api/users/<int:user_id>', 'update_user_controller', update_user_controller, methods=['PUT'])
    app.add_url_rule('/api/users/<int:user_id>', 'delete_user_controller', delete_user_controller, methods=['DELETE'])
