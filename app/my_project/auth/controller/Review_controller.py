from flask import jsonify, request
from ..dao.Review_dao import (
    create_review,
    get_review_by_id,
    get_all_reviews,
    update_review,
    delete_review
)

def get_all_reviews_controller():
    reviews = get_all_reviews()
    reviews_data = [
        {
            'id': review.id,
            'content': review.content,
            'rating': review.rating,
            'Song_id': review.Song_id,
            'User_id': review.User_id
        }
        for review in reviews
    ]
    return jsonify(reviews_data)

def get_review_controller(review_id):
    review = get_review_by_id(review_id)
    if review:
        review_data = {
            'id': review.id,
            'content': review.content,
            'rating': review.rating,
            'song_id': review.song_id,
            'user_id': review.user_id
        }
        return jsonify(review_data)
    return jsonify({'error': 'Review not found'}), 404

def add_review_controller():
    data = request.get_json()
    try:
        review = create_review(data['content'], data['rating'], data['Song_id'], data['User_id'])
        return jsonify({'message': 'Review created successfully', 'id': review.id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

def update_review_controller(review_id):
    data = request.get_json()
    try:
        review = update_review(review_id, data['content'], data['rating'])
        return jsonify({'message': 'Review updated successfully', 'id': review.id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

def delete_review_controller(review_id):
    try:
        review = delete_review(review_id)
        return jsonify({'message': 'Review deleted successfully', 'id': review.id}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500