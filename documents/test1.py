
import os
import tiktoken
import streamlit as st
from llama_index.core import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
#from langchain.chat_models import ChatOpenAI
from openai import OpenAI
from llama_index.llms.openai import OpenAI

index_name = "./saved_index"
documents_folder = "./documents/MF"

token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)
Settings.callback_manager = CallbackManager([token_counter])


#client = OpenAI()

@st.cache_resource
def initialize_index(index_name, documents_folder):
#    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    # llm_predictor = LLMPredictor(
    #     llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    # )
    service_context = ServiceContext.from_defaults(llm=llm)
    if os.path.exists(index_name):
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name),
            service_context=service_context,
        )
        print('reload')
    else:
        documents = SimpleDirectoryReader(documents_folder).load_data()
        index = GPTVectorStoreIndex.from_documents(
            documents, service_context=service_context
        )
        index.storage_context.persist(persist_dir=index_name)
        print("made index")
        print(token_counter.total_embedding_token_count)
    return index


@st.cache_data(max_entries=200, persist=True)
def query_index(_index, query_text):
    if _index is None:
        return "Please initialize the index!"
    
    retriever = index.as_retriever()
    nodes = retriever.retrieve(query_text)
    print('nodes')
    print(nodes)

    query_engine = _index.as_query_engine()
    response = query_engine.query(query_text)#"Write an email to the user given their background information.")
    print(response.get_formatted_sources())
    print('response')
    print(response)
    #print(token_counter.token_counter.total_llm_token_count)

    # response = _index.as_query_engine().query(query_text)
    # print(str(response), response)
    return str(response)
rewr
index = initialize_index(index_name, documents_folder)
#query_index(index, 'summarize this document')

st.title("🦙 111223Llama Index Demo 🦙")
st.header("Welcome to the Llama Index Streamlit Demo")
st.write(
    "Enter a query about Paul Graham's essays. You can check out the original essay [here](https://raw.githubusercontent.com/jerryjliu/llama_index/main/examples/paul_graham_essay/data/paul_graham_essay.txt). Your query will be answered using the essay as context, using embeddings from text-ada-002 and LLM completions from gpt-3.5-turbo. You can read more about Llama Index and how this works in [our docs!](https://gpt-index.readthedocs.io/en/latest/index.html)"
)

#index = None
api_key = st.text_input("Enter your OpenAI API key here:", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    index = initialize_index(index_name, documents_folder)


if index is None:
    st.warning("Please enter your api key first.")

text = st.text_input("Query text:", value="What did the author do growing up?")

if st.button("Run Query") and text is not None:
    response = query_index(index, text)
    st.markdown(response)

    llm_col, embed_col = st.columns(2)
    with llm_col:
        st.markdown(
#            f"LLM Tokens Used: {index.service_context.llm._last_token_usage}"
            "LLM Tokens Used:"# {index.service_context.llm._last_token_usage}"
        )

    print(token_counter.total_embedding_token_count)

    with embed_col:
        st.markdown(
            f"Embedding Tokens Used: {token_counter.total_embedding_token_count}"
        )