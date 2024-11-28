from flask import jsonify, request
from datetime import datetime
from ..dao.History_of_played_dao import (
    create_history_of_played,
    get_history_of_played_by_id,
    get_all_history_of_played as dao_get_all_history_of_played,
    update_history_of_played,
    delete_history_of_played as dao_delete_history_of_played,
    insert_history_of_played_in_dao
)

def serialize_entry(entry):
    """Helper function to serialize a single entry."""
    return {
        'id': entry.id,
        'date_of_playing': entry.date_of_playing.isoformat() if entry.date_of_playing else None,
        'duration': str(entry.duration) if entry.duration else None,
        'user_id': entry.user_id
    }

def get_all_history_of_played():
    """Retrieve all history of played entries."""
    history_entries = dao_get_all_history_of_played()
    history_data = [serialize_entry(entry) for entry in history_entries]
    return jsonify(history_data)

def get_history_of_played(history_id):
    """Retrieve a specific history of played entry by ID."""
    entry = get_history_of_played_by_id(history_id)
    if entry:
        return jsonify(serialize_entry(entry))
    return jsonify({'error': 'History of played entry not found'}), 404

def add_history_of_played():
    data = request.get_json()
    date_of_playing = data.get('date_of_playing')
    duration = data.get('duration')
    user_id = data.get('user_id')

    if not all([date_of_playing, duration, user_id]):
        return jsonify({'error': 'date_of_playing, duration, and user_id are required'}), 500

    try:
        date_of_playing = datetime.strptime(date_of_playing, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Incorrect date format, expected format: YYYY-MM-DD'}), 500

    result = insert_history_of_played_in_dao(date_of_playing, duration, user_id)

    if "error" in result:
        return jsonify(result), 500
    else:
        return jsonify(result), 201

def update_history_of_played(history_id):
    """Update an existing history of played entry."""
    data = request.get_json()
    date_of_playing = data.get('date_of_playing')
    duration = data.get('duration')
    user_id = data.get('user_id')

    success = update_history_of_played(history_id, date_of_playing, duration, user_id)
    if success:
        return jsonify({'message': 'History of played entry updated successfully'})
    return jsonify({'error': 'History of played entry not found'}), 404

def delete_history_of_played(history_id):
    """Delete a history of played entry by ID."""
    success = dao_delete_history_of_played(history_id)
    if success:
        return jsonify({'message': 'History of played entry deleted successfully'})
    return jsonify({'error': 'History of played entry not found'}), 404
