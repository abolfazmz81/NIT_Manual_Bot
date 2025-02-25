from elasticsearch import Elasticsearch
import config
from datetime import datetime


# Connect to Elasticsearch
es = Elasticsearch(config.port)

# Check if the Elasticsearch instance is up and running
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Elasticsearch is down!")


def create_index():
    # Create an index if it doesn't exist
    index_name = config.index_name

    # Check if the index exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Created index {index_name}")
    else:
        print(f"Index {index_name} already exists")


def index_data(question, answer):
    doc = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now(),
    }

    # Index a document
    res = es.index(index=config.index_name, document=doc)
    print(f"Indexed document: {res['_id']}")


def search_question(query):
    # Perform a search query for a question
    query_body = {
        "query": {
            "match_phrase": {
                "question": query
            }
        }
    }

    # Search in the index
    res = es.search(index=config.index_name, body=query_body)
    if len(res['hits']['hits']) ==0:
        return None
    return res['hits']['hits'][0]['_source']['answer']
