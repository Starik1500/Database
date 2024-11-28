from models import db
from sqlalchemy import text

def get_all_history_logs():
    """
    Повертає всі записи з таблиці HistoryOfPlayedLog.
    """
    try:
        result = db.session.execute(text("SELECT * FROM HistoryOfPlayedLog"))
        logs = [
            {"log_id": row[0], "history_id": row[1], "deleted_at": str(row[2])}
            for row in result.fetchall()
        ]
        return logs
    except Exception as e:
        return {"error": str(e)}

def add_history_entry(date_of_playing, duration, user_id):
    """
    Додає новий запис в таблицю history_of_played.
    """
    try:
        query = text("""
            INSERT INTO history_of_played (date_of_playing, duration, User_id)
            VALUES (:date_of_playing, :duration, :user_id)
        """)
        db.session.execute(query, {
            "date_of_playing": date_of_playing,
            "duration": duration,
            "user_id": user_id
        })
        db.session.commit()
        return {"message": "History entry added successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

def delete_history_entry(history_id):
    """
    Видаляє запис з таблиці history_of_played.
    """
    try:
        query = text("DELETE FROM history_of_played WHERE id = :history_id")
        db.session.execute(query, {"history_id": history_id})
        db.session.commit()
        return {"message": "History entry deleted successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}
