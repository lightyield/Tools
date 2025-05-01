import csv
from src.constants import CSV_HEADERS

def export_to_csv(records, output_path):
    with open(output_path, 'w', newline='', encoding='shift_jis') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for i, record in enumerate(records, start=1):
            record["取引No"] = i
            row = {key: record.get(key, "") for key in CSV_HEADERS}
            writer.writerow(row)
