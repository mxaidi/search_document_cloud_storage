import os
import uuid
from app.content_extractor import extract_text_by_extension
from app.es_indexer import ESIndexer

# Initialize
ES_HOST = "https://localhost:9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "a90vab6cA*jq2p9Utedu"
INDEX_NAME = "documents"

indexer = ESIndexer(ES_HOST, ES_USERNAME, ES_PASSWORD, INDEX_NAME)

# Extract text from files in a folder and put them in Elasticsearch
def index_files_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path):
            text = extract_text_by_extension(path)
            if not text:
                print(f"Skipping unsupported or empty: {path}")
                continue
            doc = {
                "filename": filename,
                "text": text,
                "mime_type": os.path.splitext(path)[1],
                "path": path
            }
            doc_id = str(uuid.uuid4())
            indexer.index_document(doc_id, doc)
            print(f"Indexed: {filename}")
