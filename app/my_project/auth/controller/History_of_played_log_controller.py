from flask import request, jsonify
from ..dao.History_of_played_log_dao import (
    get_all_history_logs,
    add_history_entry,
    delete_history_entry
)

def get_logs():
    """
    Отримує всі лог-записи.
    """
    logs = get_all_history_logs()
    if "error" in logs:
        return jsonify(logs), 500
    return jsonify(logs), 200

def add_history():
    """
    Додає новий запис у history_of_played.
    """
    data = request.get_json()
    date_of_playing = data.get("date_of_playing")
    duration = data.get("duration")
    user_id = data.get("user_id")

    if not all([date_of_playing, duration, user_id]):
        return jsonify({"error": "Missing required parameters"}), 400

    result = add_history_entry(date_of_playing, duration, user_id)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 201

def delete_history():
    """
    Видаляє запис з history_of_played.
    """
    data = request.get_json()
    history_id = data.get("history_id")

    if not history_id:
        return jsonify({"error": "Missing 'history_id' parameter"}), 400

    result = delete_history_entry(history_id)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200
