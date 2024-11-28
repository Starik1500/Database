from models import db, User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

ALLOWED_NAMES = ['Svitlana', 'Petro', 'Olha', 'Taras']

def prevent_invalid_name(name):
    if name not in ALLOWED_NAMES:
        raise SQLAlchemyError(f"Invalid name. Allowed names are: {', '.join(ALLOWED_NAMES)}.")

def insert_user_in_dao(name, surname, birthday, email, password, genre, currently_playing_id):
    try:
        sql = """
            INSERT INTO User (name, surname, birthday, email, password, genre, currently_playing_id)
            VALUES (:name, :surname, :birthday, :email, :password, :genre, :currently_playing_id)
        """

        db.session.execute(text(sql), {
            'name': name,
            'surname': surname,
            'birthday': birthday,
            'email': email,
            'password': password,
            'genre': genre,
            'currently_playing_id': currently_playing_id
        })

        db.session.commit()
        return {"message": "User created successfully"}

    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def create_user(name, surname, birthday, email, password, genre, currently_playing_id):
    prevent_invalid_name(name)
    insert_user_in_dao(name, surname, birthday, email, password, genre, currently_playing_id)
    return {"message": "User created successfully"}

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_all_users():
    """Returns all user entries."""
    return User.query.all()

def update_user(user_id, name, surname, birthday, email, password, genre, currently_playing_id):
    """Updates an existing user entry by its ID."""
    prevent_invalid_name(name)
    user = User.query.get(user_id)
    if user:
        user.name = name
        user.surname = surname
        user.birthday = birthday
        user.email = email
        user.password = password
        user.genre = genre
        user.currently_playing_id = currently_playing_id
        db.session.commit()
        return user
    return None

def delete_user(user_id):
    """Deletes a user entry by its ID."""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
