"""
==============================================================
Day 10 Lab: Build Your First Automated ETL Pipeline
==============================================================
Student ID: AI20K-2A202600171  (<-- Thay XXXX bang ma so cua ban)
Name: Nguyen Khanh Huyen

Nhiem vu:
   1. Extract:   Doc du lieu tu file JSON
   2. Validate:  Kiem tra & loai bo du lieu khong hop le
   3. Transform: Chuan hoa category + tinh gia giam 10%
   4. Load:      Luu ket qua ra file CSV

Cham diem tu dong:
   - Script phai chay KHONG LOI (20d)
   - Validation: loai record gia <= 0, category rong (10d)
   - Transform: discounted_price + category Title Case (10d)
   - Logging: in so record processed/dropped (10d)
   - Timestamp: them cot processed_at (10d)
==============================================================
"""

import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'


def extract(file_path):
    """
    Task 1: Doc du lieu JSON tu file.

    Goi y:
       - Dung json.load() de doc file JSON
       - Xu ly truong hop file khong ton tai (FileNotFoundError)

    Returns:
        list: Danh sach cac records (dictionaries)
    """
    print(f"Extracting data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Extract complete. {len(data)} records loaded.")
        return data

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not valid JSON.")
        return []


def validate(data):
    valid_records = []
    error_count = 0

    for record in data:
        price = record.get('price', 0)
        category = record.get('category')

        if price is None or price <= 0:
            error_count += 1
            continue

        if category is None or str(category).strip() == "":
            error_count += 1
            continue

        valid_records.append(record)

    print(f"Validation summary: {len(valid_records)} valid, {error_count} dropped")
    return valid_records


def transform(data):
    """
    Task 3: Ap dung business logic.

    Yeu cau:
       - Tinh discounted_price = price * 0.9 (giam 10%)
       - Chuan hoa category thanh Title Case (vi du: "electronics" -> "Electronics")
       - Them cot processed_at = timestamp hien tai

    Goi y:
       - Dung pd.DataFrame(data) de tao DataFrame
       - df['discounted_price'] = df['price'] * 0.9
       - df['category'] = df['category'].str.title()
       - df['processed_at'] = datetime.datetime.now().isoformat()

    Returns:
        pd.DataFrame: DataFrame da duoc transform
    """
    if not data:
        print("No valid data to transform.")
        return None

    df = pd.DataFrame(data)
    df['discounted_price'] = df['price'] * 0.9
    df['category'] = df['category'].astype(str).str.title()
    df['processed_at'] = datetime.datetime.now().isoformat()

    print(f"Transform complete. {len(df)} records processed.")
    return df


def load(df, output_path):
    """
    Task 4: Luu DataFrame ra file CSV.

    Goi y:
       - df.to_csv(output_path, index=False)
    """
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")
