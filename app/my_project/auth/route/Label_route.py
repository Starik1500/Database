from my_project.auth.controller.Label_controller import (
    get_all_labels,
    get_label,
    add_label,
    update_label,
    delete_label
)

def label_add_routes(app):
    app.add_url_rule('/api/labels', 'get_all_labels', get_all_labels, methods=['GET'])
    app.add_url_rule('/api/labels/<int:label_id>', 'get_label', get_label, methods=['GET'])
    app.add_url_rule('/api/labels', 'add_label', add_label, methods=['POST'])
    app.add_url_rule('/api/labels/<int:label_id>', 'update_label', update_label, methods=['PUT'])
    app.add_url_rule('/api/labels/<int:label_id>', 'delete_label', delete_label, methods=['DELETE'])
