from my_project.auth.controller.Review_controller import (
    get_all_reviews_controller,
    get_review_controller,
    add_review_controller,
    update_review_controller,
    delete_review_controller
)

def review_add_routes(app):
    app.add_url_rule('/api/reviews', 'get_all_reviews', get_all_reviews_controller, methods=['GET'])
    app.add_url_rule('/api/reviews/<int:review_id>', 'get_review', get_review_controller, methods=['GET'])
    app.add_url_rule('/api/reviews', 'add_review', add_review_controller, methods=['POST'])
    app.add_url_rule('/api/reviews/<int:review_id>', 'update_review', update_review_controller, methods=['PUT'])
    app.add_url_rule('/api/reviews/<int:review_id>', 'delete_review', delete_review_controller, methods=['DELETE'])