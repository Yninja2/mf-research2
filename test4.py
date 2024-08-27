import os
import base64
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
from pdf_functions import file_search_highlight_open, file_search_highlight_open_forStreamlit

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

@st.cache_resource
def display_pdf(file_path, page_number):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page={page_number}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

query_engine = initialize_index()

st.title("Welcome to MF research Demo11")
st.write("PMDAのWeb公開資料から回答を引き出します。")

text = st.text_input("質問文:", value="MFの申請時にヒト幹細胞を原材料として使用する際の注意点は?")
if st.button("回答") and text is not None:
    tab = st.tabs(["Main Tab", "PDF Tab1", "PDF Tab2", "PDF Tab3", "PDF Tab4"])
    with tab[0]:
        response = query_engine.query(text)
        file_list = []
        st.markdown('# 回答')
        st.markdown(response)
        st.markdown('___________________________________')
        for i, item in enumerate(response.source_nodes):
            print('id.....', item.node.id_)
            print('text.....', item.node.text)
            file_name =item.node.metadata['file_name']
            print('filne_name.....', item.node.metadata['file_name'],i)
            print('============================================================')
            st.markdown(f"### 検索された文章 PDF no.**{i+1}**")
            st.markdown(item.node.text)
            pdf_path, highlitedpages = file_search_highlight_open_forStreamlit(item)
            if highlitedpages == []:
                highlitedpages.append(1)
            print('pdf_path', pdf_path, highlitedpages[0])
            with tab[i+1]: 
                display_pdf(pdf_path, highlitedpages[0]+1)
            st.markdown('___________________________________')
            file_list.append(file_name)
            print(file_list)
