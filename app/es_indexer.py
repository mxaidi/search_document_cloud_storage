from elasticsearch import Elasticsearch

class ESIndexer:
    # Initialize Elasticsearch client
    def __init__(self, host, username, password, index_name="documents"):
        self.es = Elasticsearch(
            [host],
            basic_auth=(username, password),
            verify_certs=False  # Dev only
        )
        self.index_name = index_name

        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
            print(f"Index '{self.index_name}' created.")

    # Index a document using a unique id
    def index_document(self, doc_id, document):
        return self.es.index(index=self.index_name, id=doc_id, document=document)

    # Perform a search
    def search(self, query):
        body = {
            "query": {
                "match_phrase_prefix": {
                    "text": query
                }
            }
        }
        return self.es.search(index=self.index_name, body=body)

    # Retrieve all documents
    def get_all_documents(self):
        # Scroll through all documents in the index
        results = {}
        resp = self.es.search(index=self.index_name, body={"query": {"match_all": {}}}, size=1000)
        for hit in resp['hits']['hits']:
            doc_id = hit['_id']
            filename = hit['_source'].get('filename')
            results[filename] = doc_id
        return results

    # Delete documents
    def delete_document_by_filename(self, partial_filename):
        query = {
            "query": {
                "wildcard": {
                    "filename": {
                        "value": f"*{partial_filename}*",
                        "case_insensitive": True
                    }
                }
            }
        }

        result = self.es.delete_by_query(index=self.index_name, body=query)
        deleted_count = result.get("deleted", 0)
        print(f"Deleted documents with filename containing: {partial_filename}")
        return deleted_count

