import streamlit as st
import os

#api_key = st.secrets["api_key"]
print(os.environ["OPENAI_API_KEY"])# = api_key
print(os.environ["OPENAI_API_KEY"] == None )

#index = initialize_index(index_name, documents_folder)

