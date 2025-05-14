import csv
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import zipfile
import hashlib
import xml.etree.ElementTree as ET

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

def convert_file_to_zip(zip_path: str, files_to_zip: List[str], arc_names: Optional[List[str]] = None):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i, file_path in enumerate(files_to_zip):
            arcname = arc_names[i] if arc_names and i < len(arc_names) else os.path.basename(file_path)
            zipf.write(file_path, arcname=arcname)

def calculate_file_sha256(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""

    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def convert_csv_to_xml(csv_path: str, xml_path: str, root_tag: str = "Records", record_tag: str = "Record") -> bool:
    records = read_csv(csv_path)
    if not records:
        return False

    root = ET.Element(root_tag)

    for record in records:
        record_elem = ET.SubElement(root, record_tag)
        for key, value in record.items():
            field_elem = ET.SubElement(record_elem, key)
            field_elem.text = value

    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    return True


def get_next_id(filename: str) -> int:
    records = read_csv(filename)
    if not records:
        return 1
    ids = [int(record["id"]) for record in records if record["id"].isdigit()]
    return max(ids) + 1 if ids else 1

def create_record(filename: str, record: Dict[str, Any]):
    existing_records = read_csv(filename)
    fieldnames = list(record.keys())
    if existing_records:
        fieldnames = list(existing_records[0].keys())
    existing_records.append(record)
    write_csv(filename, existing_records)
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

def search_by_field(filename: str, field: str, value: str) -> List[Dict[str, Any]]:
    records = read_csv(filename)
    results = []

    for record in records:
        if field in record:
            if value.lower() in record[field].lower():
                results.append(record)
    
    return results