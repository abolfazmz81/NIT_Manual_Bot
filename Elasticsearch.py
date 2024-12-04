from elasticsearch import Elasticsearch
import config


# Connect to Elasticsearch
es = Elasticsearch(config.port)

# Check if the Elasticsearch instance is up and running
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Elasticsearch is down!")
