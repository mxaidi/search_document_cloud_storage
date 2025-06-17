import os
from app.content_extractor import extract_text_by_extension
from app.drive_connector import GoogleDriveConnector
from app.es_indexer import ESIndexer

FOLDER = "files"
ES_HOST = "https://localhost:9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "a90vab6cA*jq2p9Utedu"
INDEX_NAME = "documents"

# Initialize google Drive connector
gdc = GoogleDriveConnector()
drive_files = gdc.list_files(mime_types=[
    "text/plain",
    "text/csv",
    "application/pdf",
    "image/png"
])

drive_file_map = {f["name"]: f["id"] for f in drive_files}

indexer = ESIndexer(ES_HOST, ES_USERNAME, ES_PASSWORD, INDEX_NAME)
indexed_docs = indexer.get_all_documents()

indexed_filenames = set(indexed_docs.keys())
drive_filenames = set(drive_file_map.keys())

docs_to_delete = indexed_filenames - drive_filenames
for filename in docs_to_delete:
    indexer.delete_document_by_filename(filename)
    print(f"Deleted from index (not in Drive): {filename}")

os.makedirs(FOLDER, exist_ok=True)
for name, file_id in drive_file_map.items():
    filepath = os.path.join(FOLDER, name)
    gdc.download_file(file_id, filepath)
    text = extract_text_by_extension(filepath)
    if not text:
        continue
    doc = {
        "filename": name,
        "text": text,
        "mime_type": os.path.splitext(name)[1].lower(),
        "path": filepath
    }
    indexer.index_document(name, doc)
    print(f"Indexed: {name}")
