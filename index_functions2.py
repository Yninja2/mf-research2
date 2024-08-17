
import os
#from llama_index.core.schema import MetadataMode
from llama_index.core import (
    VectorStoreIndex,
    Settings,
    PromptTemplate,
)
from llama_index.core.callbacks import(
    CallbackManager, LlamaDebugHandler,
)

from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

import streamlit as st

class Index_function:

    try:
        qdrant_key = os.environ["qdrant_key"]
    except KeyError:
        print(f"キー は環境変数に存在しません。")
        qdrant_key = st.secrets["qdrant_key"]

    llama_debug_handler = LlamaDebugHandler()
    llama_debug_handler.get_event_pairs()
    #callback_manager = CallbackManager([llama_debug_handler])
    #service_context = ServiceContext.from_defaults(callback_manager=callback_manager)
    Settings.callback_manager = CallbackManager([llama_debug_handler])

    qa_prompt_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "answer the query in Japanese always.\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

    def set_query_engine_from_qdrant(self):
        qdrant_client = QdrantClient(
            url="https://c5c4eea7-3717-4878-a79e-25946e0c048d.us-east4-0.gcp.cloud.qdrant.io:6333",
            api_key=self.qdrant_key,
        )
        print(qdrant_client.get_collections())
        vector_store = QdrantVectorStore(client=qdrant_client, collection_name="MFdatabase")
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store,)
        query_engine = index.as_query_engine(
            response_mode = 'compact',
            similarity_top_k = 2,
            text_qa_template = self.qa_prompt_tmpl,
            verbose = True,)
            #service_context = service_context)
        return query_engine