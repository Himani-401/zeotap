from clickhouse_connect import get_client

def connect_clickhouse(config):
    client = get_client(
        host=config['host'],
        port=config['port'],
        username=config['user'],
        password=config['jwt_token'],  # using JWT as password
        database=config['database'],
        secure=True
    )
    return client

def fetch_clickhouse_columns(config):
    client = connect_clickhouse(config)
    table = config['table']
    result = client.query(f'DESCRIBE TABLE {table}')
    columns = [row[0] for row in result.result_rows]
    return columns