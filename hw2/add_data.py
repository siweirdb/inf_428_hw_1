import os
import pandas as pd
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://localhost:9200")

def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists. Skipping creation.")

def bulk_upload(file_path, index_name):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print(f"Skipped empty file: {file_path}")
            return

        # Check if the index exists before uploading
        if es.indices.exists(index=index_name):
            print(f"Index '{index_name}' already exists. Skipping upload.")
            return

        records = df.to_dict(orient="records")

        actions = [
            {
                "_index": index_name,
                "_source": record
            }
            for record in records
        ]
        helpers.bulk(es, actions)
        print(f"Uploaded {len(records)} records from {file_path} to '{index_name}'.")
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty or invalid. Skipping...")

def main():
    csv_directory = "./csv_files"

    for file_name in os.listdir(csv_directory):
        if file_name.endswith(".csv"):
            index_name = file_name.split(".")[0]
            file_path = os.path.join(csv_directory, file_name)
            print(f"Processing {file_path}...")
            create_index(index_name)
            bulk_upload(file_path, index_name)

if __name__ == "__main__":
    main()
