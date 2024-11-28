from flask import jsonify, request
from ..dao.User_dao import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from sqlalchemy.exc import SQLAlchemyError

def get_all_users_controller():
    users = get_all_users()
    users_data = [
        {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'birthday': str(user.birthday),
            'email': user.email,
            'password': user.password,
            'genre': user.genre,
            'currently_playing_id': user.currently_playing_id
        } for user in users
    ]
    return jsonify(users_data)

def get_user_controller(user_id):
    """Retrieve a user entry by its ID."""
    user = get_user_by_id(id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'birthday': str(user.birthday),
            'email': user.email,
            'password': user.password,
            'genre': user.genre,
            'currently_playing_id': user.currently_playing_id
        }
        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404

def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        birthday = data.get('birthday')
        email = data.get('email')
        password = data.get('password')
        genre = data.get('genre')
        currently_playing_id = data.get('currently_playing_id')

        result = create_user(
            name=name,
            surname=surname,
            birthday=birthday,
            email=email,
            password=password,
            genre=genre,
            currently_playing_id=currently_playing_id
        )

        return jsonify(result), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

def update_user_controller(user_id):
    """Update an existing user entry."""
    try:
        data = request.get_json()
        user = update_user(
            user_id=id,
            name=data['name'],
            surname=data['surname'],
            birthday=data['birthday'],
            email=data['email'],
            password=data['password'],
            genre=data['genre'],
            currently_playing_id=data['currently_playing_id']
        )
        if user:
            return jsonify({'message': 'User updated successfully'})
        return jsonify({'error': 'User not found'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

def delete_user_controller(user_id):
    """Delete a user entry by its ID."""
    success = delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404
