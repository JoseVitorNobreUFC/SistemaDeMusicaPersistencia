import csv
import os
from typing import List, Optional, TypeVar, Dict, Any
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

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

def create_record(filename: str, record: T):
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=record.dict().keys())
        writer.writerow(record.dict())
    return get_all_records(filename)

def get_all_records(filename: str) -> List[Dict[str, Any]]:
    return read_csv(filename)

def get_record_by_id(filename: str, record_id: str) -> Optional[Dict[str, Any]]:
    records = read_csv(filename)
    for record in records:
        if int(record["id"]) == record_id:
            return record
    return None

def update_record(filename: str, record_id: str, updated_data: T):
    records = read_csv(filename)
    updated = False
    for record in records:
        if int(record["id"]) == record_id:
            record.update(updated_data.dict())
            updated = True
            break
    if updated:
        write_csv(filename, records)
        return True
    return False

def delete_record(filename: str, record_id: str):
    records = read_csv(filename)
    filtered = [record for record in records if int(record["id"]) != record_id]
    if len(filtered) != len(records):
        write_csv(filename, filtered)
        return True
    return False
