from flask import jsonify, request
from datetime import datetime
from sqlalchemy import text
from models import db
from ..dao.Currently_playing_dao import (
    create_currently_playing,
    get_currently_playing_by_id,
    get_all_currently_playing as dao_get_all_currently_playing,
    delete_currently_playing as dao_delete_currently_playing,
    insert_currently_playing
)

def get_all_currently_playing():
    """Retrieve all currently playing entries."""
    currently_playing_list = dao_get_all_currently_playing()
    currently_playing_data = [
        {
            'id': entry.id,
            'is_played_now': entry.is_played_now,
            'timestamp': entry.timestamp,
            'device': entry.device,
            'song_id': entry.song_id
        }
        for entry in currently_playing_list
    ]
    return jsonify(currently_playing_data)

def get_currently_playing(currently_playing_id):
    """Retrieve a currently playing entry by ID."""
    entry = get_currently_playing_by_id(currently_playing_id)
    if entry:
        entry_data = {
            'id': entry.id,
            'is_played_now': entry.is_played_now,
            'timestamp': entry.timestamp,
            'device': entry.device,
            'song_id': entry.song_id
        }
        return jsonify(entry_data)
    return jsonify({'error': 'Currently playing entry not found'}), 404

def add_currently_playing():
    data = request.get_json()
    is_played_now = data.get('is_played_now')
    timestamp_str = data.get('timestamp')
    device = data.get('device')
    song_id = data.get('song_id')

    if not all([is_played_now, timestamp_str, device, song_id]):
        return jsonify({'error': 'is_played_now, timestamp, device, and song_id are required'}), 400

    try:
        timestamp = datetime.strptime(timestamp_str, '%a, %d %b %Y %H:%M:%S %Z')
    except ValueError:
        return jsonify({'error': 'Incorrect date format, expected format: Tue, 10 Oct 2023 13:00:00 GMT'}), 400

    result = insert_currently_playing_in_controller(is_played_now, timestamp, device, song_id)

    if "error" in result:
        return jsonify(result), 500
    else:
        return jsonify(result), 201

def update_currently_playing(currently_playing_id):
    """Update an existing currently playing entry."""
    data = request.get_json()
    entry = get_currently_playing_by_id(currently_playing_id)
    if not entry:
        return jsonify({'error': 'Currently playing entry not found'}), 404

    entry.is_played_now = data.get('is_played_now', entry.is_played_now)
    entry.timestamp = data.get('timestamp', entry.timestamp)
    entry.device = data.get('device', entry.device)
    entry.song_id = data.get('song_id', entry.song_id)

    db.session.commit()
    return jsonify({'message': 'Currently playing entry updated successfully'})

def delete_currently_playing(currently_playing_id):
    """Delete a currently playing entry by ID."""
    success = dao_delete_currently_playing(currently_playing_id)
    if success:
        return jsonify({'message': 'Currently playing entry deleted successfully'})
    return jsonify({'error': 'Currently playing entry not found'}), 404


def insert_currently_playing_in_controller(is_played_now, timestamp, device, song_id):
    try:
        sql = text("""
            INSERT INTO Currently_playing (is_played_now, timestamp, device, song_id)
            VALUES (:is_played_now, :timestamp, :device, :song_id)
        """)

        db.session.execute(sql, {
            'is_played_now': is_played_now,
            'timestamp': timestamp,
            'device': device,
            'song_id': song_id
        })

        db.session.commit()
        return {"message": "Currently playing entry created successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to insert record: {str(e)}"}
