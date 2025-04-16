from clickhouse_driver import Client
import pandas as pd
import csv

def connect_clickhouse(config):
    return Client(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

def get_clickhouse_tables(client):
    return [row[0] for row in client.execute("SHOW TABLES")]

def get_table_columns(client, table):
    result = client.execute(f"DESCRIBE TABLE {table}")
    return [row[0] for row in result]

def export_to_csv(client, query, filename="output.csv"):
    result = client.execute(query)
    if not result:
        return 0
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)
    return len(result)

def import_csv_to_clickhouse(file_path, client, table_name):
    df = pd.read_csv(file_path)
    records = [tuple(row) for row in df.values]
    columns = ', '.join(df.columns)
    query = f"INSERT INTO {table_name} ({columns}) VALUES"
    client.execute(query, records)
    return len(records)

def preview_clickhouse_data(client, table, columns, limit=100):
    cols = ', '.join(columns)
    result = client.execute(f"SELECT {cols} FROM {table} LIMIT {limit}")
    return result
