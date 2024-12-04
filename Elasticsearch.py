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


# Index some sample Q&A data (you can customize this)
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
