from ingestion.clickhouse_connector import connect_clickhouse
from ingestion.file_handler import write_csv, read_csv

def ingest_clickhouse_to_file(config):
    client = connect_clickhouse(config)
    table = config['table']
    columns = config['columns']
    file_path = config['file_name']
    delimiter = config.get('delimiter', ',')

    col_str = ', '.join(columns)
    query = f"SELECT {col_str} FROM {table}"
    result = client.query(query)
    
    # Write to CSV
    write_csv(file_path, columns, result.result_rows, delimiter)
    return len(result.result_rows)

def ingest_file_to_clickhouse(config):
    client = connect_clickhouse(config)
    file_path = config['file_name']
    table = config['target_table']
    delimiter = config.get('delimiter', ',')
    selected_columns = config['columns']

    # Read data from file
    headers, rows = read_csv(file_path, delimiter)

    # Only select requested columns
    indices = [headers.index(col) for col in selected_columns]
    filtered_rows = [[row[i] for i in indices] for row in rows]

    # Construct query
    col_str = ', '.join(selected_columns)
    placeholders = ', '.join(['%s'] * len(selected_columns))
    insert_query = f"INSERT INTO {table} ({col_str}) VALUES"

    # Insert
    client.insert(table, filtered_rows, column_names=selected_columns)
    return len(filtered_rows)