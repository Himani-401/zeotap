# utils.py
from clickhouse_driver import Client
import json

def connect_to_clickhouse(config):
    """
    Connect to ClickHouse using the given config dictionary.
    """
    try:
        client = Client(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return client, None
    except Exception as e:
        return None, str(e)

def fetch_tables(client):
    """
    Fetch the list of tables in the connected ClickHouse database.
    """
    try:
        tables = client.execute('SHOW TABLES')
        return [table[0] for table in tables]
    except Exception as e:
        return None, str(e)

def fetch_columns(client, table):
    """
    Fetch the column names of a specific table.
    """
    try:
        columns = client.execute(f"DESCRIBE TABLE {table}")
        return [column[0] for column in columns]
    except Exception as e:
        return None, str(e)

def ingest_flat_file_to_clickhouse(client, table, file_path, delimiter):
    """
    Ingest data from a Flat File (CSV/TSV) to a ClickHouse table.
    """
    import pandas as pd
    try:
        # Read the flat file (CSV/TSV) using pandas
        df = pd.read_csv(file_path, delimiter=delimiter)
        
        # Prepare the data for ClickHouse insertion
        data = df.values.tolist()
        columns = df.columns.tolist()

        # Insert data into ClickHouse
        client.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES", data)
        return len(data), None
    except Exception as e:
        return None, str(e)
