from flask import jsonify, request
from ..dao.User_dao import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)

def get_all_users_controller():
    """Retrieve all user entries."""
    users = get_all_users()
    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'birthday': user.birthday,
            'email': user.email,
            'genre': user.genre,
            'currently_playing_id': user.currently_playing_id
        }
        for user in users
    ]
    return jsonify(users_data)

def get_user_controller(user_id):
    """Retrieve a user entry by its ID."""
    user = get_user_by_id(user_id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'birthday': user.birthday,
            'email': user.email,
            'genre': user.genre,
            'currently_playing_id': user.currently_playing_id
        }
        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404

def add_user():
    """Add a new user entry."""
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    birthday = data.get('birthday')
    email = data.get('email')
    password = data.get('password')
    genre = data.get('genre')
    currently_playing_id = data.get('currently_playing_id')

    if not all([name, surname, birthday, email, password, genre]):
        return jsonify({'error': 'name, surname, birthday, email, password, and genre are required'}), 400

    user = create_user(name, surname, birthday, email, password, genre, currently_playing_id)
    return jsonify({
        'message': 'User created successfully',
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'email': user.email
    }), 201

def update_user_controller(user_id):
    """Update an existing user entry."""
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    birthday = data.get('birthday')
    email = data.get('email')
    password = data.get('password')
    genre = data.get('genre')
    currently_playing_id = data.get('currently_playing_id')

    user = update_user(user_id, name, surname, birthday, email, password, genre, currently_playing_id)
    if user:
        return jsonify({'message': 'User updated successfully', 'id': user.id})
    return jsonify({'error': 'User not found'}), 404

def delete_user_controller(user_id):
    """Delete a user entry by its ID."""
    success = delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404
