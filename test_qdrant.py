from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os

try:
    qdrant_key = os.environ["qdrant_key"]
except KeyError:
    print(f"キー は環境変数に存在しません。")

qdrant_client = QdrantClient(
    url="https://c5c4eea7-3717-4878-a79e-25946e0c048d.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key= qdrant_key)

print(qdrant_client.get_collections())

vector_store = QdrantVectorStore(client=qdrant_client, collection_name="MFdatabase")
#storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,)
query_engine = index.as_query_engine()

response = query_engine.query("残留溶媒について教えてください。日本語で回答してください")
print(response)