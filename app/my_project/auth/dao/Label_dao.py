from models import db, Label
from sqlalchemy import text

def insert_label_in_dao(name, country):
    """Параметризована вставка для таблиці 'Label'."""
    try:
        sql = text("""
            INSERT INTO Label (name, country)
            VALUES (:name, :country)
        """)

        # Виконання параметризованого SQL-запиту
        db.session.execute(sql, {
            'name': name,
            'country': country
        })

        db.session.commit()  # Коміт змін у базі даних
        return {"message": "Label created successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to insert record: {str(e)}"}

def create_label(name, country):
    """Creates a new label."""
    label = Label(name=name, country=country)
    db.session.add(label)
    db.session.commit()
    return label

def get_label_by_id(label_id):
    """Retrieves a label by its ID."""
    return Label.query.get(label_id)

def get_all_labels():
    """Returns all labels."""
    return Label.query.all()

def update_label(label_id, name, country):
    """Updates an existing label by its ID."""
    label = Label.query.get(label_id)
    if label:
        label.name = name
        label.country = country
        db.session.commit()
        return label
    return None

def delete_label(label_id):
    """Deletes a label by its ID."""
    label = Label.query.get(label_id)
    if label:
        db.session.delete(label)
        db.session.commit()
        return True
    return False
