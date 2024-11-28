from flask import jsonify, request
from ..dao.for_all_dao import aggregate_column, create_dynamic_tables

def aggregate_column_route():
    data = request.get_json()

    table_name = data.get("table_name")
    column_name = data.get("column_name")
    agg_function = data.get("agg_function")

    if not all([table_name, column_name, agg_function]):
        return jsonify({"error": "Missing one or more parameters: table_name, column_name, agg_function"}), 400

    result = aggregate_column(table_name, column_name, agg_function)

    if "error" in result:
        return jsonify(result), 500

    return jsonify(result), 200


def create_tables_controller():
    data = request.get_json()
    source_table_name = data.get("source_table_name")
    column_name = data.get("column_name")

    if not source_table_name or not column_name:
        return jsonify({"error": "Missing source_table_name or column_name"}), 400

    result = create_dynamic_tables(source_table_name, column_name)

    if 'error' in result:
        return jsonify(result), 500

    return jsonify(result), 200