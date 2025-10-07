from models import db, Review, Song, User
from sqlalchemy.exc import IntegrityError

def get_all_reviews():
    """Отримує всі відгуки."""
    return Review.query.all()

def get_review_by_id(review_id):
    """Отримує відгук за ID."""
    return Review.query.filter_by(id=review_id).first()

def validate_song_exists(Song_id):
    """Перевіряє існування пісні."""
    song = Song.query.get(Song_id)
    if not song:
        raise ValueError(f"Invalid Song_id: The song with ID {Song_id} does not exist.")
    return song

def validate_user_exists(User_id):
    user = User.query.get(User_id)
    if not user:
        raise ValueError(f"Invalid User_id: The user with ID {User_id} does not exist.")
    return user

def create_review(content, rating, Song_id, User_id):
    validate_song_exists(Song_id)
    validate_user_exists(User_id)

    new_review = Review(content=content, rating=rating, Song_id=Song_id, User_id=User_id)

    try:
        db.session.add(new_review)
        db.session.commit()
        return new_review
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError(f"Error while adding review: {e}")

def update_review(review_id, content, rating):
    """Оновлює існуючий відгук."""
    review = get_review_by_id(review_id)
    if not review:
        raise ValueError(f"Review with ID {review_id} not found.")

    review.content = content
    review.rating = rating
    review.validate_rating()
    db.session.commit()
    return review

def delete_review(review_id):
    """Видаляє відгук за ID."""
    review = get_review_by_id(review_id)
    if not review:
        raise ValueError(f"Review with ID {review_id} not found.")
    db.session.delete(review)
    db.session.commit()
    return review
