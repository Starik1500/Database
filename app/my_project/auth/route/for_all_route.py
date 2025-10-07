from flask_jwt_extended import jwt_required
from my_project.auth.controller.for_all_controller import (
    aggregate_column_route, create_tables_controller, get_token_controller
)

def for_all_add_routes(app):
        app.add_url_rule('/get-token', 'get_token', get_token_controller, methods=['POST'])
        app.add_url_rule('/api/aggregate_column', 'aggregate_column_route', jwt_required()(aggregate_column_route), methods=['POST'])
        app.add_url_rule('/api/create_dynamic_tables', 'create_tables_controller', jwt_required()(create_tables_controller), methods=['POST']
    )
