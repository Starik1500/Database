from models import db
from sqlalchemy import text
from flask import Flask, jsonify
import random

def aggregate_column(table_name, column_name, agg_function):
    try:
        query = text(f"SELECT {agg_function}({column_name}) FROM {table_name}")

        result = db.session.execute(query).fetchone()

        if result:
            return {"result": result[0]}
        else:
            return {"error": "No results found"}

    except Exception as e:
        return {"error": str(e)}


def create_dynamic_tables(source_table_name, column_name):
    try:
        create_temp_table_query = text(f"""
                CREATE TEMPORARY TABLE dynamic_source AS
                SELECT DISTINCT {column_name} AS col_value FROM {source_table_name}
            """)
        db.session.execute(create_temp_table_query)
        db.session.commit()

        cursor_query = text("""
                SELECT DISTINCT CONCAT(REPLACE(col_value, ' ', '_'), '_', UNIX_TIMESTAMP()) AS table_name
                FROM dynamic_source
            """)
        result = db.session.execute(cursor_query)

        for row in result:
            table_name = row[0]
            column_count = random.randint(1, 9)

            create_table_query = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY"

            for i in range(1, column_count + 1):
                col_name = f"col_{i}"
                col_type = random.choice(['INT', 'VARCHAR(255)', 'DOUBLE'])
                create_table_query += f", {col_name} {col_type}"

            create_table_query += ')'

            db.session.execute(text(create_table_query))
            db.session.commit()

        db.session.execute(text("DROP TEMPORARY TABLE IF EXISTS dynamic_source"))
        db.session.commit()

        return {"message": "Dynamic tables created successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}