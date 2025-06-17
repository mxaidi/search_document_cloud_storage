from flask import Flask, request, jsonify
from es_indexer import ESIndexer
import uuid

app = Flask(__name__)

ES_HOST = "https://localhost:9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "a90vab6cA*jq2p9Utedu"
INDEX_NAME = "documents"

indexer = ESIndexer(ES_HOST, ES_USERNAME, ES_PASSWORD, INDEX_NAME)

# Define a route for searching documents
@app.route("/search", methods=["GET"])
def search():
    # Extract files
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Missing search query parameter 'q'"}), 400

     # Perform search using the Elasticsearch
    response = indexer.search(query)
    hits = response.get("hits", {}).get("hits", [])

    filepaths = []
    for hit in hits:
        source = hit.get("_source", {})
        path = source.get("path")
        if path:
            filepaths.append(path)

    return jsonify({"results": filepaths})

if __name__ == "__main__":
    app.run(debug=True)
