from flask import Flask, request, jsonify
from flask_cors import CORS  

from ingestion import connect_clickhouse, export_to_csv, import_csv_to_clickhouse, get_clickhouse_tables, get_table_columns, preview_clickhouse_data

app = Flask(__name__)

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    try:
        client = connect_clickhouse(data)
        return jsonify({"message": "Connected successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/clickhouse/tables', methods=['POST'])
def list_tables():
    data = request.json
    client = connect_clickhouse(data)
    tables = get_clickhouse_tables(client)
    return jsonify({"tables": tables})

@app.route('/clickhouse/columns', methods=['POST'])
def list_columns():
    data = request.json
    table = data['table']
    client = connect_clickhouse(data)
    columns = get_table_columns(client, table)
    return jsonify({"columns": columns})

@app.route('/ingest/ch-to-file', methods=['POST'])
def ch_to_file():
    data = request.json
    client = connect_clickhouse(data)
    query = data['query']
    filename = data.get('filename', 'output.csv')
    count = export_to_csv(client, query, filename)
    return jsonify({"message": f"Exported {count} records to {filename}."})

@app.route('/ingest/file-to-ch', methods=['POST'])
def file_to_ch():
    data = request.json
    client = connect_clickhouse(data)
    file_path = data['file_path']
    table_name = data['table_name']
    count = import_csv_to_clickhouse(file_path, client, table_name)
    return jsonify({"message": f"Ingested {count} records from {file_path} to {table_name}."})

@app.route('/preview', methods=['POST'])
def preview_table():
    data = request.json
    try:
        conn = connect_clickhouse(data)
        table = data.get("table")
        columns = data.get("columns", [])
        if not columns:
            return jsonify({"error": "No columns selected"}), 400

        preview_data = preview_clickhouse_data(conn, table, columns)
        return jsonify({"preview": preview_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)
