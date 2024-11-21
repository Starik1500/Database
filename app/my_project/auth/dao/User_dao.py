from models import db, User

def create_user(name, surname, birthday, email, password, genre, currently_playing_id):
    """Creates a new user entry."""
    user = User(
        name=name,
        surname=surname,
        birthday=birthday,
        email=email,
        password=password,
        genre=genre,
        currently_playing_id=currently_playing_id
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id):
    """Retrieves a user entry by its ID."""
    return User.query.get(user_id)

def get_all_users():
    """Returns all user entries."""
    return User.query.all()

def update_user(user_id, name, surname, birthday, email, password, genre, currently_playing_id):
    """Updates an existing user entry by its ID."""
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
