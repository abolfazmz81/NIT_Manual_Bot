import extractor
import weaviate
from langchain_openai import ChatOpenAI
import config
from weaviate.classes.config import Property, DataType

# Add embedding model
llm = ChatOpenAI(model="text-embedding-ada-002	", base_url="https://api.avalai.ir/v1",
                 api_key=config.embedder_token)

# Connect to Weaviate
client = weaviate.connect_to_local()
print(client.is_ready())

# Get documents to use as Section
ayin97 = extractor.return_97("docs/1633766767-ayinnamehkarshenasi97-v3.pdf")
ayin402 = extractor.return_97("docs/66914c6472fb4-1402.pdf")
ayin97 = "این آیین نامه برای ورودی 97 تا 401 صادق است: \n" + ayin97
ayin402 = "این آیین نامه برای ورودی 402 به بعد صادق است: \n" + ayin402

# Create the schema
try:
    # Create the class in Weaviate
    client.collections.create("ChatDocs", properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="content", data_type=DataType.TEXT),
    ])
    print("Schema created!")
except:
    print("schema already exists or an unexpected error happened")

client.close()
