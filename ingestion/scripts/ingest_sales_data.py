import os
import pandas as pd
import boto3
from datetime import datetime, timezone
import logging

# --- CONFIG ---
#resetting the script to use 3 different data files

DATA_FILES = {
    "invoices": {
        "path": "/Users/papayaw/projects/qle_pipeline/retail_ingestion/test_data/invoices.csv",
        "expected_columns": [
            'invoice_id', 'customer_id', 'item_id',
            'quantity', 'rate', 'amount',
            'invoice_date', 'due_date', 'status'
        ]
    },
    "customers": {
        "path": "/Users/papayaw/projects/qle_pipeline/retail_ingestion/test_data/customers.csv",
        "expected_columns": [
            'customer_id', 'customer_name', 'email',
            'phone', 'region', 'created_date', 'customer_type'
        ]
    },
    "items": {
        "path": "/Users/papayaw/projects/qle_pipeline/retail_ingestion/test_data/items.csv",
        "expected_columns": [
            'item_id', 'item_name', 'item_type',
            'category', 'unit_price', 'taxable'
        ]
    }
}

LOG_FILE = '/Users/papayaw/projects/qle_pipeline/retail_ingestion/logs/ingestion_log.csv'
S3_BUCKET = 'qle-retail-pipeline'  
S3_PREFIX = 'raw'
REGION = 'us-east-2'             

# --- SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- VALIDATE DATA ---
def validate_csv(filepath, expected_columns):
    df = pd.read_csv(filepath)
    if list(df.columns) != expected_columns:
        raise ValueError(f"Schema mismatch in {filepath}.")
    logging.info(f"Validated schema of {filepath}")
    return df

# --- UPLOAD TO S3 ---
def upload_to_s3(filepath, bucket, dataset_name):
    today = datetime.today()
    s3_key = f"{S3_PREFIX}/{dataset_name}/year={today.year}/month={today.month:02}/day={today.day:02}/{os.path.basename(filepath)}"

    s3 = boto3.client("s3", region_name=REGION)
    s3.upload_file(filepath, bucket, s3_key)
    logging.info(f"Uploaded to s3://{bucket}/{s3_key}")
    return s3_key

# --- LOG METADATA LOCALLY ---
def log_metadata(dataset_name, filename, row_count, s3_key):
    now = datetime.now(timezone.utc).isoformat()
    log_entry = {
        "dataset": dataset_name,
        "filename": filename,
        "row_count": row_count,
        "s3_key": s3_key,
        "status": "success",
        "timestamp": now
    }

    # 🔐 Ensure the directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    log_df = pd.DataFrame([log_entry])
    header = not os.path.exists(LOG_FILE)
    log_df.to_csv(LOG_FILE, mode='a', header=header, index=False)
    logging.info("Ingestion log updated.")

# --- MAIN FUNCTION ---
def main():
    logging.info("Starting multi-dataset ingestion...")

    for dataset, config in DATA_FILES.items():
        try:
            df = validate_csv(config['path'], config['expected_columns'])
            s3_key = upload_to_s3(config['path'], S3_BUCKET, dataset)
            log_metadata(dataset, os.path.basename(config['path']), len(df), s3_key)
        except Exception as e:
            logging.error(f"Failed to ingest {dataset}: {e}")

    logging.info("Ingestion completed for all datasets.")

# --- RUN ---
if __name__ == "__main__":
    main()
