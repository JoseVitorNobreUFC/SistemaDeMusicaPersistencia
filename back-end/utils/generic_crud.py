import csv
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

def read_csv(filename: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filename):
        return []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(filename: str, data: List[Dict[str, Any]]):
    if data:
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def get_next_id(filename: str) -> int:
    records = read_csv(filename)
    if not records:
        return 1
    ids = [int(record["id"]) for record in records if record["id"].isdigit()]
    return max(ids) + 1 if ids else 1

def create_record(filename: str, record: Dict[str, Any]):
    fieldnames = list(record.keys())
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(record)
    return get_all_records(filename)

def get_all_records(filename: str) -> List[Dict[str, Any]]:
    return read_csv(filename)

def get_record_by_id(filename: str, record_id: int) -> Optional[Dict[str, Any]]:
    records = read_csv(filename)
    for record in records:
        if int(record["id"]) == record_id:
            return record
    return None

def update_record(filename: str, record_id: int, updated_data: Dict[str, Any]):
    records = read_csv(filename)
    updated = False

    for i, record in enumerate(records):
        if int(record["id"]) == record_id:
            updated_record = {
                "id": record_id,
                **updated_data  # sobrescreve os dados antigos
            }
            records[i] = updated_record
            updated = True
            break

    if updated:
        fieldnames = list(records[0].keys())  # manter a ordem do primeiro registro
        write_csv(filename, records)
        return True
    return False

def delete_record(filename: str, record_id: int):
    records = read_csv(filename)
    filtered = [record for record in records if int(record["id"]) != record_id]
    if len(filtered) != len(records):
        write_csv(filename, filtered)
        return True
    return False
