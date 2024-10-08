
import os
import tiktoken
import streamlit as st
from index_functions2 import Index_function
from llama_index.core import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
from llama_index.llms.openai import OpenAI

# setting for API_key of OpenAI
try:
    value = os.environ["OPENAI_API_KEY"]
except KeyError:
    print(f"キー は環境変数に存在しません。")
    os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]

Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)
#Settings.callback_manager = CallbackManager([token_counter])

@st.cache_resource
def initialize_index():#index_name, documents_folder):
    print('initilizing......')
    index_function = Index_function()
    query_engine = index_function.set_query_engine_from_qdrant()#make_query_engine()
    return query_engine

query_engine = initialize_index()

st.title("Welcome to MF research Demo11")
st.write("PMDAのWeb公開資料から回答を引き出します。")

text = st.text_input("質問文:", value="MFの申請時にヒト幹細胞を原材料として使用する際の注意点は?")

if st.button("回答") and text is not None:
    response = query_engine.query(text)
    st.markdown('# 回答')
    st.markdown(response)
    st.markdown('___________________________________')
    for item in response.source_nodes:
        #print(item)
        name = item.node.metadata['file_name'].split('.')[-2][4:] # file name extract
        print('id', item.node.id_)
        print('text', item.node.text)
        print('filne_name', item.node.metadata['file_name'])
        print('============================================================')
        url = 'https://www.pmda.go.jp/files/' + name + '.pdf'
        text = item.node.text # extract source text
        #point_id = item.node
        st.markdown("### 根拠となる資料")
        st.markdown("### " + url)
        st.markdown("### 関連する文章")
        st.markdown(text)
        st.markdown('___________________________________')
