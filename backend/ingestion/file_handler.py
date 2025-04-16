import csv

def write_csv(file_path, headers, data, delimiter=','):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(headers)
        writer.writerows(data)

def read_csv(file_path, delimiter=','):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)
        headers = rows[0]
        data = rows[1:]
    return headers, data