from flask import jsonify, request
from ..dao.User_dao import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from sqlalchemy.exc import SQLAlchemyError
from flasgger import swag_from

@swag_from({
    'tags': ['Users'],
    'responses': {
        200: {
            'description': 'List of all users',
            'examples': {
                'application/json': [
                    {
                        'id': 1,
                        'name': 'John',
                        'surname': 'Doe',
                        'birthday': '1990-01-01',
                        'email': 'john@example.com',
                        'password': 'hashedpassword',
                    }
                ]
            }
        }
    }
})

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
        } for user in users
    ]
    return jsonify(users_data)

@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the user to retrieve'
        }
    ],
    'responses': {
        200: {'description': 'User found'},
        404: {'description': 'User not found'}
    }
})

def get_user_controller(user_id):
    """Retrieve a user entry by its ID."""
    user = get_user_by_id(user_id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'birthday': str(user.birthday),
            'email': user.email,
            'password': user.password,
        }
        return jsonify(user_data)
    return jsonify({'error': 'User not found'}), 404


@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'surname': {'type': 'string'},
                    'birthday': {'type': 'string', 'example': '1990-01-01'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                },
                'required': ['name', 'surname', 'birthday', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'Invalid input'}
    }
})

def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        birthday = data.get('birthday')
        email = data.get('email')
        password = data.get('password')

        result = create_user(
            name=name,
            surname=surname,
            birthday=birthday,
            email=email,
            password=password,
        )

        return jsonify(result), 201
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 400

@swag_from({
    'tags': ['Users'],
    'parameters': [
        {'name': 'user_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'surname': {'type': 'string'},
                    'birthday': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'User updated successfully'},
        404: {'description': 'User not found'}
    }
})

def update_user_controller(user_id):
    """Update an existing user entry."""
    try:
        data = request.get_json()
        user = update_user(
            user_id=user_id,
            name=data['name'],
            surname=data['surname'],
            birthday=data['birthday'],
            email=data['email'],
            password=data['password'],
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
